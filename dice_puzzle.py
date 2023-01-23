import numpy as np

grid = [[57,33,132,268,492,732],[81,123,240,443,353,508],[186,42,195,704,452,228],[-7,2,357,452,317,395],[5,23,-4,592,445,620],[0,77,32,403,337,452]]
visited_squares = np.zeros((6,6))
visited_squares[5][0] = 1

# top, back, left, right, front, bottom
dice = [None]*6

def move_dice(dice, direction):
    if direction == 0:   # up
        new_dice = [dice[4], dice[0], dice[2], dice[3], dice[5], dice[1]]
    elif direction == 1: # right
        new_dice = [dice[2], dice[1], dice[5], dice[0], dice[4], dice[3]]
    elif direction == 2: # down
        new_dice = [dice[1], dice[5], dice[2], dice[3], dice[0], dice[4]]
    elif direction == 3: # left
        new_dice = [dice[3], dice[1], dice[0], dice[5], dice[4], dice[2]]
    return new_dice

def rec_check_square(dice, depth, current_pos, score, visited, path):
    current_score = 0

    if depth != 0:
        if max(current_pos[0], current_pos[1]) > 5 or min(current_pos[0], current_pos[1]) < 0:
            return False

        visited[current_pos[0]][current_pos[1]] = 1
        path.append((current_pos[0],current_pos[1]))
        
        if dice[0] == None:
            dice[0] = (grid[current_pos[0]][current_pos[1]] - score) / depth

        current_score = score + depth*dice[0]
        if current_score != grid[current_pos[0]][current_pos[1]]:
            return False

        if current_pos == [0,5]:
            print(f"Done! The dice sides are {dice}\nthe path it took was\n{path}\nand the visited squares were \n{visited}")
            return True
    
    rec_check_square(move_dice(dice,0), depth+1, [current_pos[0], current_pos[1] + 1], current_score, visited, path[:])
    rec_check_square(move_dice(dice,1), depth+1, [current_pos[0] + 1, current_pos[1]], current_score, visited, path[:])
    rec_check_square(move_dice(dice,2), depth+1, [current_pos[0], current_pos[1] - 1], current_score, visited, path[:])
    rec_check_square(move_dice(dice,3), depth+1, [current_pos[0] - 1, current_pos[1]], current_score, visited, path[:])

rec_check_square(dice, 0, [5,0], 0, visited_squares, [(5,0)])
