import math
import timeit
import random

# shellSort
def shellSort(a, p_x, p_y):
    N = len(a)
    h = 1
    while h < N / 3:
        h = 3 * h + 1   # Knuth's Sequence 1, 4, 13, 40, 121, 364, ...

    while h >= 1:        
        hInsertionSort(a, h, p_x, p_y)
        h = h // 3
    
    return a

# hInsertion Sort for convexHull
def hInsertionSort(a, h, p_x, p_y):
    for i in range(h, len(a)):  # Begin from a[h]
        data = a[i]
        key = math.atan2(a[i][1] - p_y, a[i][0] - p_x)     # Element to move at current iteration
        j = i - h
        while j >= 0 and math.atan2(a[j][1] - p_y, a[j][0] - p_x) > key:
                a[j + h] = a[j]  # Move element a[j] to a[j+h] if a[j] > key
                j -= h         # Decrement j by h
        a[j + h] = data   # Place the key to the farthest it can go to the left      
    return a

# ccw
def ccw(i, j, k):
    area2 = (j[0] - i[0]) * (k[1] - i[1]) - (j[1] - i[1]) * (k[0] - i[0])
    if area2 > 0: return True #convex
    else: return False #concave

# Given a list of points (x, y)
# find the convex hull using Graham's Scan
# Return a list of points in the convex hull in ccw order
def grahamScan(points):

    # find p
    p_x = None
    p_y = None
    for i in range(len(points)):
        if(p_x == None):
            p_x = points[i][0]
            p_y = points[i][1]
        elif(p_y > points[i][1]):
            p_x = points[i][0]
            p_y = points[i][1]
        elif(p_y == points[i][1]):
            if(p_x < points[i][0]):
                p_x = points[i][0]
                p_y = points[i][1]

    # sort
    shellSort(points, p_x, p_y)

    # convexHull
    convex = []
    for i in range(len(points)):
        if(len(convex) < 2):
            convex.append(points[i])
        else:
            while(ccw(convex[len(convex)-2], convex[len(convex)-1], points[i]) == False): # concave
                convex.pop()
                if(len(convex) == 1):
                    break
            # convex
            convex.append(points[i])

    # final check
    while(ccw(convex[len(convex)-2], convex[len(convex)-1], points[0]) == False):
        convex.pop()

    return convex


def correctnessTest(input, expected_output, correct):
    output = grahamScan(input)
    print(f"grahamScan({input})\n{output}")
    if output == expected_output: print("Pass")
    else:        
        print(f"Fail - expected output: {expected_output}")
        correct = False
    print()    

    return correct


def simulateNSquare(points):    
    points = sorted(points, key = lambda p: (p[1], -p[0]))     
    for i in range(len(points)):
        points_with_angle = []
        for j in range(i + 1, len(points)):
            x, y = points[j]
            points_with_angle.append((x, y, math.atan2(y - points[i][1], x - points[i][0])))
        points_with_angle = sorted(points_with_angle, key = lambda p: p[2])


'''
Unit Test
'''
if __name__ == "__main__":
    '''# ccw turns
    print(ccw((0,0), (-1,1), (-2, -1)))
    print(ccw((-1,1), (-2, -1), (0,0)))
    print(ccw((-2, -1), (0,0), (-1,1)))

    # non-ccw turns
    print(ccw((0,0), (-2, -1), (-1,1)))
    print(ccw((-2, -1), (-1,1), (0,0)))
    print(ccw((-1,1), (0,0), (-2, -1)))
    print(ccw((0,0), (-1, 1), (-2, 2))) # Straight line'''

    print("Correctness test for grahamScan()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True
    
    input = [(3, -1), (2, -2), (4, -1)]
    expected_output = [(2, -2), (4, -1), (3, -1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(0, 0), (-2, -1), (-1, 1), (1, -1), (3, -1), (-3, -1)]
    expected_output = [(3, -1), (-1, 1), (-3, -1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(4, 2), (3, -1), (2, -2), (1, 0), (0, 2), (0, -2), (-1, 1), (-2, -1), (-2, -3), (-3, 3), (-4, 0), (-4, -1), (-4, -2), (-4, -3), (-4, -4)]
    expected_output = [(-4, -4), (2, -2), (3, -1), (4, 2), (-3, 3), (-4, 0)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(2, 0), (2, 2), (1, -1), (0, 2), (-1, 1), (-2, -2)]
    expected_output = [(-2, -2), (1, -1), (2, 0), (2, 2), (0, 2), (-1, 1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(2, 0), (2, 2), (1, -1), (0, 2), (-1, 1), (-2, -2), (-2, 2), (4, -4)]
    expected_output = [(4, -4), (2, 2), (-2, 2), (-2, -2)]
    correct = correctnessTest(input, expected_output, correct)

    # "342235" is a 6-digit number and is greater than the other 5-digit numbers
    input = [(342235, -23412), (-74545, 72345), (25812, -45689), (-45676, 24578), (45689, 0), (-74545, 0), (0, 45689), (0, -45689)]
    expected_output = [(25812, -45689), (342235, -23412), (-74545, 72345), (-74545, 0), (0, -45689)]
    correct = correctnessTest(input, expected_output, correct)
    
    print()
    print("Speed test for grahamScan()")
    if not correct: print("Fail (since the algorithm is not correct)")
    else:
        repeat = 10
        inputLength = 100
        minC, maxC = -1000000, 1000000
        points = [(random.randint(minC, maxC), random.randint(minC, maxC)) for _ in range(inputLength)]
        tCodeToCompare = timeit.timeit(lambda: simulateNSquare(points), number=repeat) / repeat
        tSubmittedCode = timeit.timeit(lambda: grahamScan(points), number=repeat) / repeat        
        print(f"Average running time of grahamScan() and simulateNSquare() * 0.2 with {inputLength} points: {tSubmittedCode:.10f} and {tCodeToCompare * 0.2:.10f}")                
        if tSubmittedCode < tCodeToCompare * 0.2: print("Pass")
        else:
            print("Fail")
        print() 