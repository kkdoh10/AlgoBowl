import math
from numpy import arange
from Cell import Cell
from Cell import Type
import random as rand
import time
import copy

def count_adjacent_lights(map, row, col):
    count = 0

    if row > 0 and map[row-1][col].type == Type.LIGHT:
        count+=1
    if row < len(map) - 1 and map[row+1][col].type == Type.LIGHT:
        count+=1
    if col > 0 and map[row][col-1].type == Type.LIGHT:
        count+=1
    if col < len(map[row]) - 1 and map[row][col+1].type == Type.LIGHT:
        count+=1
    return count
def assign_map(og_map, new_map):
    rows = len(og_map)
    cols = len(og_map[0])
    new_map = [[0]*cols for r in range(rows)]
    for r in range(rows):
        for c in range(cols):
            new_map[r][c] = og_map[r][c].deepcopy()
def objective(map, row, col):
    violations = 0
    for r in range(0, row):
        for c in range(0, col):
            adjacent_lights = count_adjacent_lights(map, r, c)
            #violation for blank cell i.e. not lit => super high violation count bc invalid output
            if map[r][c].type == Type.BLANK:
                found_light = False
                left = c-1
                while not found_light and 0 <= left:
                    if map[r][left].type == Type.LIGHT:
                        found_light = True
                        break
                    elif map[r][left].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
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
                    elif map[up][c].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    up = up-1
                    
                down = r + 1
                while not found_light and len(map) > down:
                    if map[down][c].type == Type.LIGHT:
                        found_light = True
                        break
                    elif map[down][c].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    down = down+1
                    
                if not found_light:
                    #print("--------------------no light---------------")
                    #print(str(r) + " " + str(c))
                    #print_map(map)
                    return row*col*100000000000
            #violations for grey cells    
            elif map[r][c].type == Type.GREY0 and adjacent_lights != 0:
                violations+=1
            elif map[r][c].type == Type.GREY1 and adjacent_lights != 1:
                violations+=1
            elif map[r][c].type == Type.GREY2 and adjacent_lights != 2:
                violations+=1
            elif map[r][c].type == Type.GREY3 and adjacent_lights != 3:
                violations+=1    
            elif map[r][c].type == Type.GREY4 and adjacent_lights != 4:
                violations+=1
            #violations for light
            elif map[r][c].type == Type.LIGHT:
                light_violation = 0
                left = c-1
                while 0 <= left:
                    if map[r][left].type == Type.LIGHT:
                        light_violation+=1
                        break
                    if map[r][left].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    left = left-1
                
                right = c+1
                while len(map[r]) > right:
                    if map[r][right].type == Type.LIGHT:
                        light_violation+=1
                        break
                    if map[r][right].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    right = right+1
                    
                up = r - 1
                while 0 <= up:
                    if map[up][c].type == Type.LIGHT:
                        light_violation+=1
                        break
                    if map[up][c].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    up = up-1
                    
                down = r + 1
                while len(map) > down:
                    if map[down][c].type == Type.LIGHT:
                        light_violation+=1
                        break
                    if map[down][c].type  in {Type.GREY, Type.GREY0, Type.GREY1, Type.GREY2, Type.GREY3, Type.GREY4}:
                        break
                    down = down+1
                if light_violation > 0: violations+=1
    return violations


def simulated_annealing(grid, rows, cols, max_iterations: int =100, cooling_rate: float =.999, initial_temp: int = 1000):
    current_grid = [row[:] for row in grid]
    for r in range(rows):
        for c in range(cols):
            #if current_grid[r][c].type == Type.BLANK:#  and rand.random() < 0.5:
            if current_grid[r][c].type == Type.BLANK  and rand.random() < 0.5:
                current_grid[r][c].type = Type.LIGHT

    current_violations = objective(current_grid, rows, cols)
  
    
    best_grid = current_grid
    best_violations = current_violations
    
    temp = initial_temp
    for iteration in range(max_iterations):
        neighbor_soln = [row[:] for row in current_grid]
        
        r, c = rand.randint(0, rows - 1), rand.randint(0, cols - 1)
        while neighbor_soln[r][c].type not in {Type.BLANK, Type.LIGHT}:
            r, c = rand.randint(0, rows - 1), rand.randint(0, cols - 1)
        if neighbor_soln[r][c].type == Type.BLANK:
            neighbor_soln[r][c].type = Type.LIGHT
        elif neighbor_soln[r][c].type == Type.LIGHT:
            neighbor_soln[r][c].type = Type.BLANK
        
        neighbor_violations = objective(neighbor_soln, rows, cols)

        if neighbor_violations < current_violations:
            current_grid = copy.deepcopy(neighbor_soln)
            current_violations = neighbor_violations
            if current_violations < best_violations:
                best_grid = copy.deepcopy(current_grid)
                best_violations = current_violations
        else:
            acceptance_probability = math.exp((current_violations - neighbor_violations) / temp)
            if rand.random() < acceptance_probability:
                #assign_map(current_grid, neighbor_soln)
                current_grid = copy.deepcopy(neighbor_soln)
                current_violations = neighbor_violations

        if best_violations == rows*cols*100000000000:
            iteration = iteration-10
        
        temp *=cooling_rate
    
    return best_violations, best_grid 