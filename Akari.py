import math
from numpy import arange
from Cell import Cell
from Cell import Type
import random as rand

def count_adjacent_lights(map, row, col):
    count = 0

    if row != 0:
        if map[row-1][col].type == Type.LIGHT:
            count+=1
    if map[row+1][col].type == Type.LIGHT:
        count+=1
    if map[row][col-1].type == Type.LIGHT:
        count+=1
    if map[row][col+1].type == Type.LIGHT:
        count+=1
    return count

def objective(map, row, col):
    violations = 0
    for r in range(0, row-1):
        for c in range(0, col-1):
            if map[r][c].type == Type.BLANK:
                found_light = False
                left = c-1
                while not found_light and 0 <= left:
                    if map[r][left].type == Type.LIGHT:
                        found_light = True
                    if map[r][left].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    left = left-1
                
                right = c+1
                while not found_light and len(map[r]) > right:
                    if map[r][right].type == Type.LIGHT:
                        found_light = True
                        break
                    elif map[r][right].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    right = right+1
                    
                up = r - 1
                while not found_light and 0 <= up:
                    if map[up][c].type == Type.LIGHT:
                        found_light = True
                        break
                    if map[up][c].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    up = up-1
                    
                down = r + 1
                while not found_light and len(map) > down:
                    if map[down][c].type == Type.LIGHT:
                        found_light = True
                        break
                    if map[down][c].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    down = down+1
                    
                if not found_light:
                    return row*col*100000000000
                
            if map[r][c].type == Type.GREY0 and count_adjacent_lights(map, r, c) != 0:
                violations+=1
            if map[r][c].type == Type.GREY1 and count_adjacent_lights(map, r, c) != 1:
                violations+=1
            if map[r][c].type == Type.GREY2 and count_adjacent_lights(map, r, c) != 2:
                violations+=1
            if map[r][c].type == Type.GREY3 and count_adjacent_lights(map, r, c) != 3:
                violations+=1    
            if map[r][c].type == Type.GREY4 and count_adjacent_lights(map, r, c) != 4:
                violations+=1
            if map[r][c].type == Type.LIGHT:
                left = c-1
                while 0 <= left:
                    if map[r][left].type == Type.LIGHT:
                        violations+=1
                    if map[r][left].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    left = left-1
                
                right = c+1
                while len(map[r]) > right:
                    if map[r][right].type == Type.LIGHT:
                        violations+=1
                    if map[r][right].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    right = right+1
                    
                up = r - 1
                while 0 <= up:
                    if map[up][c].type == Type.LIGHT:
                        violations+=1
                    if map[up][c].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    up = up-1
                    
                down = r + 1
                while len(map) > down:
                    if map[down][c].type == Type.LIGHT:
                        violations+=1
                    if map[down][c].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    down = down+1
    return violations
def print_map(map):
    for r in map:
        row = ''.join(cell.type.value for cell in r) 
        print(row)

def simulated_annealing(grid, rows, cols, max_iterations: int =100, cooling_rate: float =.999, initial_temp: int = 1000):
    current_grid = [row[:] for row in grid]
    
    current_grid = [row[:] for row in grid]
    for r in range(rows):
        for c in range(cols):
            if current_grid[r][c].type == Type.BLANK:#  and rand.random() < 0.5:
                current_grid[r][c].type = Type.LIGHT

    
    current_violations = objective(current_grid, rows, cols)
    best_grid = current_grid
    best_violations = current_violations
    
    
    temp = initial_temp
    for iteration in range(max_iterations):
        print(current_violations)
        #print_map(current_grid)
        neighbor_soln = [row[:] for row in current_grid]
        

        i, j = rand.randint(0, rows - 1), rand.randint(0, cols - 1)
        if neighbor_soln[i][j].type == Type.BLANK:
            neighbor_soln[i][j].type = Type.LIGHT
        if neighbor_soln[i][j].type == Type.LIGHT:
            neighbor_soln[i][j].type = Type.BLANK

        
        neighbor_violations = objective(neighbor_soln, rows, cols)
        
        if neighbor_violations < current_violations:
            current_grid =neighbor_soln
            current_violations =neighbor_violations
        else:
            acceptance_probability = math.exp((current_violations - neighbor_violations) / temp)
            if rand.random() < acceptance_probability:
                current_grid = neighbor_soln
                current_violations =neighbor_violations
        
        if current_violations < best_violations:
            best_grid = current_grid
            best_violations = current_violations

            temp *=cooling_rate
    return best_violations, best_grid