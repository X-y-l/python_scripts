import numpy as np
import pygame as pg
import random
import math

# to add:
# maze gens: sidewinder, ellers, prims, backtrack, wilsons, hunt & kill
# maze solvers: right hand rule, left hand rule, A*, dijkstras

# is solving from start and end simultaneously better?

# can I incorperate music into maze algorithms somehow? (sort of like sorting algorithms)

# a "river" measure, ie how long corridoors tend to be from a given algorithm
# a twistyness measure, ie maximum stack depth required by a recursive backtracker
# a difficulty measure, ie a sort of heuristic using combination of twistiness,
# solution length, 

# cellular automata: only check specific neighbours based on position (x+y mod 4, fan shape)?
# random neighbour check?

# function that turns the rulestring for a lifelike cellular automaton (ie B3/S23) and decomposes it into two lists (ie [3], [2,3])
def code_str_to_lists(code):
    code = code.split("/")
    births, survives = [int(x) for x in [*code][0][1:]], [int(y) for y in [*code][1][1:]]
    print(births, survives)
    return births, survives


# randomizes the radius by radius square in the middle of a grid of cells (randomly chooses to set them as 0s or 1s)
def randomize_center(cells, radius):
    height, width = len(cells), len(cells[0])
    for y in range(math.floor(height/2 - radius), math.ceil(height/2 + radius)):
        for x in range(math.floor(width/2 - radius), math.ceil(width/2 + radius)):
            cells[y][x] = random.randint(0,1)


# sums up the value of cells in the Moore neighbourhood of a given cell
def sum_surrounding_cells(cells, x, y):
    return np.sum(cells[np.ix_([y-1,y,y+1],[x-1,x,x+1])]) - cells[y][x]


# performs one step of a life-like cellular automaton
def lifelike_step(cells, birth, survive):
    height, width = len(cells), len(cells[0])
    newgrid = np.zeros((height, width))
    for y in range(1, height-1):
        for x in range(1, width-1):
            neighbours = sum_surrounding_cells(cells, x, y)
            if neighbours in birth and cells[y][x] == 0:
                newgrid[y][x] = 1
            elif neighbours in survive and cells[y][x] == 1:
                newgrid[y][x] = cells[y][x]
            else:
                newgrid[y][x] = 0
    return newgrid


# takes a grid of cells and draws them to the screen with the corresponding colour
def draw_cells(cells, cols, cell_size, screen):
    for y, line in enumerate(cells):
        for x, cell in enumerate(line):
            pg.draw.rect(screen, cols[int(cell)], (x*cell_size, y*cell_size, cell_size, cell_size))


# takes the lists containing wall locations, and turns it into a grid of cells where each cell is either a path or a wall.
def maze_to_cells(maze):
    vert_walls, horiz_walls = maze[0], maze[1]
    cells_height, cells_width = 2*len(vert_walls) + 1, 2*len(horiz_walls[0])+1
    cells = np.zeros((cells_height, cells_width))

    for y in range(1, cells_height-1):
        for x in range(1, cells_width-1):
            if x % 2 == 1 and y % 2 == 1:
                cells[y][x] = 1
    
            elif x % 2 == 1 and y % 2 == 0:
                cells[y][x] = horiz_walls[int((y-2)/2)][int((x-1)/2)]
            
            elif x % 2 == 0 and y % 2 == 1:
                cells[y][x] = vert_walls[int((y-1)/2)][int((x-2)/2)]

    return cells


# generates a "maze" where it randomly chooses each wall to be either on or off
def random_maze(width, height):
    horiz_walls = np.random.randint(0, 2, size=(height-1, width))
    vert_walls = np.random.randint(0, 2, size=(height, width-1))

    maze = [vert_walls, horiz_walls]
    return maze


# generates a maze using recursive division
def gen_maze_recur_div(width, height):
    horiz_walls = np.zeros((height-1, width))
    vert_walls = np.zeros((height, width-1))

    if width == 1 and height == 1:
        return vert_walls, horiz_walls
    elif width == 1:
        split_across = 1
    elif height == 1:
        split_across = 0
    else:
        split_across = (random.random() <= height/(width+height))

    if split_across:
        split = random.randint(0, height-2) # lock y value - horizontal line
        gap = random.randint(0, width-1)

        horiz_walls[split][gap] = 1

        # Top
        new_vert, new_horiz = gen_maze_recur_div(width, split+1)

        if (new_vert.shape[1] != 0):
            vert_walls[:new_vert.shape[0], -new_vert.shape[1]:] = new_vert
        if (new_horiz.shape[0] != 0):
            horiz_walls[:new_horiz.shape[0], -new_horiz.shape[1]:] = new_horiz

        # Bottom
        new_vert, new_horiz = gen_maze_recur_div(width, height-(split+1))

        if (new_vert.shape[1] != 0):
            vert_walls[-new_vert.shape[0]:, -new_vert.shape[1]:] = new_vert
        if (new_horiz.shape[0] != 0):
            horiz_walls[-new_horiz.shape[0]:, -new_horiz.shape[1]:] = new_horiz

    else:
        split = random.randint(0, width-2) # lock x value - vert line
        gap = random.randint(0, height-1)

        vert_walls[gap][split] = 1

        # Left
        new_vert, new_horiz = gen_maze_recur_div(split+1, height)

        if (new_vert.shape[1] != 0):
            vert_walls[:new_vert.shape[0], :new_vert.shape[1]] = new_vert
        if (new_horiz.shape[0] != 0):
            horiz_walls[:new_horiz.shape[0], :new_horiz.shape[1]] = new_horiz
        
        # Right
        new_vert, new_horiz = gen_maze_recur_div(width-(split+1), height)

        if (new_vert.shape[1] != 0):
            vert_walls[:new_vert.shape[0], -new_vert.shape[1]:] = new_vert
        if (new_horiz.shape[0] != 0):
            horiz_walls[:new_horiz.shape[0], -new_horiz.shape[1]:] = new_horiz

    return vert_walls, horiz_walls


# generates a maze using the Aldous-Broder algorithm
def gen_maze_aldous_broder(width, height):
    grid = np.zeros((height,width))
    horiz_walls = np.zeros((height-1, width))
    vert_walls = np.zeros((height, width-1))
    vects = [[1,0], [-1,0], [0,1], [0,-1]]

    current_cell = [0, 0] # x,y
    grid[current_cell[1]][current_cell[0]] = 1

    while np.sum(grid) != width * height: # while not all cells have been visited
        direction = vects[random.randint(0,3)]
        current_cell = np.add(current_cell,direction)

        if not (current_cell[1] in [-1, height] or current_cell[0] in [-1, width]): # makes sure inside borders
            if grid[current_cell[1]][current_cell[0]] != 1: # not yet visited

                if direction in [[1,0], [-1,0]]: # moving right or left
                    vert_walls[current_cell[1]][current_cell[0] - (direction == [1,0])] = 1

                else:                            # moving up or down
                    horiz_walls[current_cell[1] - (direction == [0,1])][current_cell[0]] = 1

                grid[current_cell[1]][current_cell[0]] = 1 # set as visited

        else: # if fell outside borders, move it back
            current_cell = np.add(current_cell, np.negative(direction))

    return vert_walls, horiz_walls


# generates a maze using the binary tree algorithm
def gen_maze_bin_tree(width, height):
    horiz_walls = np.zeros((height-1, width))
    vert_walls = np.zeros((height, width-1))

    for y in range(height):
        for x in range(width):
            if not (y == height - 1 and x == width - 1):
                if y == height - 1:
                    vert_walls[y][x] = 1
                elif x == width - 1:
                    horiz_walls[y][x] = 1
                elif random.random() < 0.5: # carve right
                    vert_walls[y][x] = 1
                else:                       # carve down
                    horiz_walls[y][x] = 1

    return vert_walls, horiz_walls


# generates a maze using the recursive backtracking algorithm
def gen_maze_recur_backtrack(width, height):
    horiz_walls = np.zeros((height-1, width))
    vert_walls = np.zeros((height, width-1))
    grid = np.zeros((height, width))
    visited_stack = []
    current_cell = [random.randint(0,width-1), random.randint(0,height-1)]
    visited_stack.append(current_cell)
    grid[current_cell[1]][current_cell[0]] = 1

    vects = [[1,0], [-1,0], [0,1], [0,-1]]

    while visited_stack != []: # while not all cells have been visited
        current_cell = visited_stack.pop()
        possible_neighbours = []
        
        for vect in vects:
            if not (current_cell[1] + vect[1] in [-1, height] or current_cell[0] + vect[0] in [-1, width]):
                if grid[current_cell[1] + vect[1]][current_cell[0] + vect[0]] == 0:
                    possible_neighbours.append([current_cell[0] + vect[0], current_cell[1] + vect[1]])

        if possible_neighbours != []:
            visited_stack.append(current_cell)
            next_cell = random.choice(possible_neighbours)
            direction = [current_cell[0] - next_cell[0],  current_cell[1] - next_cell[1]]

            if direction in [[1,0], [-1,0]]:
                vert_walls[current_cell[1]][current_cell[0] - (direction == [1,0])] = 1
            else:
                horiz_walls[current_cell[1] - (direction == [0,1])][current_cell[0]] = 1

            current_cell = next_cell
            grid[current_cell[1]][current_cell[0]] = 1
            visited_stack.append(current_cell)

    return vert_walls, horiz_walls


def gen_maze_kruskal(width, height):
    horiz_walls = np.zeros((height-1, width))
    vert_walls = np.zeros((height, width-1))
    connected_cells = []

    for x in range(width):
        for y in range(height):
            connected_cells.append([[x,y]])

    rand_wall_index = np.arange(0, 2*width*height - width - height, 1)
    np.random.shuffle(rand_wall_index)

    while len(connected_cells) > 1:
        current_wall_index, rand_wall_index = rand_wall_index[-1], rand_wall_index[:-1]
        cell_groups = []

        if current_wall_index < width * (height - 1): # select horiz wall
            current_wall = [current_wall_index % width, current_wall_index // width]

            for group in connected_cells:
                if len(cell_groups) > 1:
                    break
                for cell in group:
                    if cell in [[current_wall[0], current_wall[1]],[current_wall[0], current_wall[1]+1]]:
                        cell_groups.append(group)

            if cell_groups[0] != cell_groups[1]:
                horiz_walls[current_wall[1]][current_wall[0]] = 1
                connected_cells.remove(cell_groups[0]); connected_cells.remove(cell_groups[1])
                connected_cells.append(cell_groups[0] + cell_groups[1])

        else: # select vert wall
            current_wall_index -= width * (height - 1)
            current_wall = [current_wall_index % (width-1), current_wall_index // (width-1)]
            
            for group in connected_cells:
                if len(cell_groups) > 1:
                    break
                for cell in group:
                    if cell in [[current_wall[0], current_wall[1]],[current_wall[0]+1, current_wall[1]]]:
                        cell_groups.append(group)

            if cell_groups[0] != cell_groups[1]:
                vert_walls[current_wall[1]][current_wall[0]] = 1
                connected_cells.remove(cell_groups[0]); connected_cells.remove(cell_groups[1])
                connected_cells.append(cell_groups[0] + cell_groups[1])

    return vert_walls, horiz_walls


# takes a grid of cells representing a maze and makes holes at the top left and bottom right,
# representing the entrance and exit to the maze
def add_openings(cells):
    cells[0][1] = 1
    cells[-1][-2] = 1
    return cells


# maze solving algorithm that works by repeatedly filling in dead ends
def solve_maze_dead_end_step(cells):
    hei, wid = len(cells), len(cells[0])
    newgrid = np.zeros((hei, wid))
    vects = [(1,0),(0,1),(-1,0),(0,-1)]

    for y in range(1, hei-1):
        for x in range(1, wid-1):

            if cells[y][x] == 1:
                neighbours = 0
                for vect in vects:
                    if cells[y+vect[0]][x+vect[1]] in [0,2]:
                        neighbours += 1
            
                if neighbours in [3,4]:
                    newgrid[y][x] = 2
                else:
                    newgrid[y][x] = 1
            
            else:
                newgrid[y][x] = cells[y][x]

    newgrid[0][1] = 1
    newgrid[-1][-2] = 1
    return newgrid
 

def main():
    cell_size = 8
    dimensions = maze_width, maze_height = 100, 50
    cells = maze_to_cells(gen_maze_kruskal(maze_width, maze_height))
    add_openings(cells)

    pg.init()
    screen_width, screen_height = len(cells[0]) * cell_size, len(cells) * cell_size
    screen_size = [screen_width, screen_height]
    screen = pg.display.set_mode(screen_size)
    pg.display.set_caption("Automata stuff")
    clock = pg.time.Clock()

    done = False

    while not done:
        clock.tick(60)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        screen.fill((0,0,0))
        cells = solve_maze_dead_end_step(cells)
        draw_cells(cells, [(0,0,0), (255,255,255), (150,150,150)], cell_size, screen)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()