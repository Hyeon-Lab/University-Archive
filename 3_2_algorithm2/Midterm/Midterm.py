from queue import PriorityQueue


def ManhattanDistance(x, y, gx, gy, min_cell_cost):
    if(gx-x > 0):
        dx = gx-x
    else:
        dx = x-gx
    if(gy-y > 0):
        dy = gy-y
    else:
        dy = y-gy
    return (dx + dy) * min_cell_cost

def findMinCostPath(cost, sx, sy, gx, gy):
    '''
    INPUT:
        cost: 2D array for cell costs
        sx, sy: x and y of the source
        gx, gy: x and y of the goal

    OUTPUT:
        (1) cost sum of the minimum-cost path, except the source
        (2) list of coordinates in the minimum-cost path
    '''
    minPQ = PriorityQueue()

    n = len(cost[0])
    min_cell_cost =  cost[0][0]
    for i in range(len(cost)):
        for j in range(len(cost)):
            if(cost[i][j] <= min_cell_cost):
                min_cell_cost = cost[i][j]
    x = sx
    y = sy
    cur_cost = 0
    ex = None
    total_cost = 0
    result = []
    minPQ.put((cur_cost + ManhattanDistance(x, y, gx, gy, min_cell_cost), x, y, cur_cost, ex))
    while(True):
        cur = minPQ.get()
        (cur_expect, cur_x, cur_y, cur_cost, cur_ex) = cur
        #print("!!get cur", cur)

        if((cur_x == gx) & (cur_y == gy)):
            break
        
        if(cur_x-1 >= 0):
            if(cur_ex == None):
                minPQ.put((cur_cost + cost[cur_y][cur_x-1] + ManhattanDistance(cur_x-1, cur_y, gx, gy, min_cell_cost), cur_x-1, cur_y, cost[cur_y][cur_x-1] + cur_cost, cur))
                #print("!!put0", (cur_cost + cost[y][x-1] + ManhattanDistance(cur_x-1, cur_y, gx, gy, min_cell_cost), cur_x-1, cur_y, cur_cost + cost[y][x-1], cur))
            elif((cur_ex[1] != cur_x-1) | (cur_ex[2] != cur_y)):
                minPQ.put((cur_cost + cost[cur_y][cur_x-1] + ManhattanDistance(cur_x-1, cur_y, gx, gy, min_cell_cost), cur_x-1, cur_y, cost[cur_y][cur_x-1] + cur_cost, cur))
                #print("!!put0", (cur_cost + cost[y][x-1] + ManhattanDistance(cur_x-1, cur_y, gx, gy, min_cell_cost), cur_x-1, cur_y, cur_cost + cost[y][x-1], cur))  
            
        if(cur_x+1 <= n-1):
            if(cur_ex == None):
                minPQ.put((cur_cost + cost[cur_y][cur_x+1] + ManhattanDistance(cur_x+1, cur_y, gx, gy, min_cell_cost), cur_x+1, cur_y, cost[cur_y][cur_x+1] + cur_cost, cur))
                #print("!!put1", (cur_cost + cost[y][x+1] + ManhattanDistance(cur_x+1, cur_y, gx, gy, min_cell_cost), cur_x+1, cur_y, cur_cost + cost[y][x+1], cur))
        
            elif((cur_ex[1] != cur_x+1) | (cur_ex[2] != cur_y)):
                minPQ.put((cur_cost + cost[cur_y][cur_x+1] + ManhattanDistance(cur_x+1, cur_y, gx, gy, min_cell_cost), cur_x+1, cur_y, cost[cur_y][cur_x+1] + cur_cost, cur))
                #print("!!put1", (cur_cost + cost[y][x+1] + ManhattanDistance(cur_x+1, cur_y, gx, gy, min_cell_cost), cur_x+1, cur_y, cur_cost + cost[y][x+1], cur))
        
        if(cur_y-1 >= 0):
            if(cur_ex == None):
                minPQ.put((cur_cost + cost[cur_y-1][cur_x] + ManhattanDistance(cur_x, cur_y-1, gx, gy, min_cell_cost), cur_x, cur_y-1, cost[cur_y-1][cur_x] + cur_cost, cur))
                #print("!!put2", (cur_cost + cost[y-1][x] + ManhattanDistance(cur_x, cur_y-1, gx, gy, min_cell_cost), cur_x, cur_y-1, cur_cost + cost[y-1][x], cur))

            elif((cur_ex[1] != cur_x) | (cur_ex[2] != cur_y-1)):
                minPQ.put((cur_cost + cost[cur_y-1][cur_x] + ManhattanDistance(cur_x, cur_y-1, gx, gy, min_cell_cost), cur_x, cur_y-1, cost[cur_y-1][cur_x] + cur_cost, cur))
                #print("!!put2", (cur_cost + cost[y-1][x] + ManhattanDistance(cur_x, cur_y-1, gx, gy, min_cell_cost), cur_x, cur_y-1, cur_cost + cost[y-1][x], cur))

        if(cur_y+1 <= n-1):
            if(cur_ex == None):
                minPQ.put((cur_cost + cost[cur_y+1][cur_x] + ManhattanDistance(cur_x, cur_y+1, gx, gy, min_cell_cost), cur_x, cur_y+1, cost[cur_y+1][cur_x] + cur_cost, cur))
                #print("!!put3", (cur_cost + cost[y+1][x] + ManhattanDistance(cur_x, cur_y+1, gx, gy, min_cell_cost), cur_x, cur_y+1, cur_cost + cost[y+1][x], cur))
            
            elif((cur_ex[1] != cur_x) | (cur_ex[2] != cur_y+1)):
                minPQ.put((cur_cost + cost[cur_y+1][cur_x] + ManhattanDistance(cur_x, cur_y+1, gx, gy, min_cell_cost), cur_x, cur_y+1, cost[cur_y+1][cur_x] + cur_cost, cur))
                #print("!!put3", (cur_cost + cost[y+1][x] + ManhattanDistance(cur_x, cur_y+1, gx, gy, min_cell_cost), cur_x, cur_y+1, cur_cost + cost[y+1][x], cur))

    #print(cur)

    result.append((sx, sy))
    total_cost = cur[3]
    while(cur[4] != None):
        result.insert(1, (cur[1], cur[2]))
        cur = cur[4]

    return total_cost, result


def correctnessTest(func, input, expected_cost, expected_list, correct):
    print(f"{func.__name__}({input})")
    output = func(*input)
    print(f"output:{output}")
    cost, path = output
    if not (isinstance(cost, int) and 0 <= cost):
        print(f"Fail - the first token of the output must be an integer >= 0")
        correct = False
    elif not isinstance(path, list):
        print(f"Fail - the second token of the output must be a list")
        correct = False
    else:
        if expected_list is None:
            if expected_cost == cost: print("Pass")
            else:
                print(f"Fail - the output cost ({cost}) not match the expected cost ({expected_cost})")
                correct = False                            
        else:
            if expected_cost == cost and expected_list == path: print("Pass")
            else:    
                print(f"Fail - the output does not match the expected output ({expected_cost}, {expected_list})")
                correct = False                            
    print()    

    return correct


if __name__ == "__main__":
    '''
    Unit Test
    '''    
    print("Correctness test for midterm()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True

    correct = correctnessTest(findMinCostPath, ([[1, 1, 1],\
                                                 [1, 1, 1],\
                                                 [1, 1, 1]], 1, 1, 1, 1), 0, [(1, 1)], correct) 

    correct = correctnessTest(findMinCostPath, ([[1, 1, 1],\
                                                 [1, 1, 1],\
                                                 [1, 1, 1]], 0, 0, 2, 0), 2, [(0, 0), (1, 0), (2, 0)], correct)

    correct = correctnessTest(findMinCostPath, ([[1, 9, 1, 1],\
                                                 [1, 9, 1, 1],\
                                                 [1, 2, 1, 9],\
                                                 [9, 9, 1, 1]], 0, 0, 3, 3), 7, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (3, 3)], correct)

    correct = correctnessTest(findMinCostPath, ([[1, 1, 9, 9, 9, 9],\
                                                 [1, 1, 1, 1, 9, 9],\
                                                 [9, 1, 9, 1, 1, 1],\
                                                 [9, 1, 1, 1, 9, 1],\
                                                 [9, 9, 9, 1, 1, 1]], 0, 0, 5, 4), 9, None, correct)
    # several minimum-cost paths exist (e.g., [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (4, 4), (5, 4)])

    correct = correctnessTest(findMinCostPath, ([[1, 2, 3, 4, 5, 6, 7, 8, 9],\
                                                 [9, 9, 9, 9, 9, 9, 9, 9, 9],\
                                                 [9, 8, 7, 6, 5, 4, 3, 2, 1],\
                                                 [9, 9, 9, 9, 9, 9, 9, 9, 9],\
                                                 [1, 2, 3, 4, 5, 6, 7, 8, 9]], 0, 0, 8, 4), 56, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4)], correct)
    
    