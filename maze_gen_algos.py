import numpy as np
import pygame as pg
import random
import math

# to add:
# maze gens: sidewinder, ellers, prims, kruskals, recursive backtrack, wilsons
# maze solvers: right hand rule, left hand rule, A*, 

# a "river" measure, ie how long corridoors tend to be from a given algorithm

def code_str_to_lists(code):
    code = code.split("/")
    births, survives = [int(x) for x in [*code][0][1:]], [int(y) for y in [*code][1][1:]]
    print(births, survives)
    return births, survives


def randomize_center(cells, radius):
    for y in range(math.floor(maze_height/2 - radius), math.floor(maze_height/2 + radius)):
        for x in range(math.floor(maze_width/2 - radius), math.floor(maze_width/2 + radius)):
            cells[y][x] = random.randint(0,1)


def sum_surrounding_cells(cells, x, y):
    return np.sum(cells[np.ix_([y-1,y,y+1],[x-1,x,x+1])]) - cells[y][x]


def lifelike_step(cells, birth, survive):
    newgrid = np.zeros((maze_height, maze_width))
    for y in range(1, maze_height-1):
        for x in range(1, maze_width-1):
            neighbours = sum_surrounding_cells(cells, x, y)
            if neighbours in birth and cells[y][x] == 0:
                newgrid[y][x] = 1
            elif neighbours in survive and cells[y][x] == 1:
                newgrid[y][x] = cells[y][x]
            else:
                newgrid[y][x] = 0
    return newgrid


def draw_cells(cells):
    for y, line in enumerate(cells):
        for x, cell in enumerate(line):
            if cell == 1:
                pg.draw.rect(screen, (255,255,255), (x*cell_size, y*cell_size, cell_size, cell_size))
            if cell == 2:
                pg.draw.rect(screen, (0,255,0), (x*cell_size, y*cell_size, cell_size, cell_size))


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


def random_maze(width, height):
    horiz_walls = np.random.randint(0, 2, size=(height-1, width))
    vert_walls = np.random.randint(0, 2, size=(height, width-1))

    maze = [vert_walls, horiz_walls]
    return maze


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


def gen_maze_aldous_broder(width, height):
    grid = np.zeros((height,width))
    horiz_walls = np.zeros((height-1, width))
    vert_walls = np.zeros((height, width-1))
    vects = [[1,0], [-1,0], [0,1], [0,-1]]

    current_cell = [0, 0] # x,y
    grid[current_cell[1]][current_cell[0]] = 1

    while np.sum(grid) != width * height:
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


def add_openings(cells):
    cells[0][1] = 1
    cells[-1][-2] = 1
    return cells


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
 

cell_size = 10
maze_width, maze_height = 50,25
cells = maze_to_cells(gen_maze_bin_tree(maze_width, maze_height))
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
    draw_cells(cells)

    pg.display.flip()

pg.quit()