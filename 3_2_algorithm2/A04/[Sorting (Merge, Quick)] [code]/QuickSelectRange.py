import random
import timeit

# Partition a[lo~hi] into 3-sections and then continue to partition each half recursively
def partition3Way(a, lo, hi, k, m):
    if (hi <= lo): return
    v = a[lo]
    lt, gt = lo, hi  # Indices to put next items <v and >v    
    i = lo
    while i <= gt:
        if a[i] < v:
            a[lt], a[i] = a[i], a[lt]  # Swap
            lt, i = lt+1, i+1
        elif a[i] > v:
            a[gt], a[i] = a[i], a[gt]  # Swap
            gt = gt-1
        else: i = i+1

    if(k < lt) & (m < lt):
        partition3Way(a, lo, lt-1, k, m)
    elif(k > gt) & (m > gt):
        partition3Way(a, gt+1, hi, k, m)
    else:
        partition3Way(a, lo, lt-1, k, m)
        partition3Way(a, gt+1, hi, k, m)
    

def quickSelect(a, k, m):
    
    random.shuffle(a)

    partition3Way(a, 0, len(a)-1, k, m)
    return a[k:m + 1]


def speedCompare(a):
    def recur(a, lo, hi):
        if hi <= lo: return

        i, j = lo+1, hi
        while True:
            while i <= hi and a[i] < a[lo]: i = i+1
            while j >= lo+1 and a[j] > a[lo]: j = j-1

            if (j <= i): break
            a[i], a[j] = a[j], a[i]
            i, j = i+1, j-1
        a[lo], a[j] = a[j], a[lo]        
           
        recur(a, lo, j-1)
        recur(a, j+1, hi)

    random.shuffle(a)
    recur(a, 0, len(a)-1)
    return a


def testCorrectness(a, k, m, expectedOutput, correct, output2console):    
    print(f"Correctness test for selecting {m-k+1} out of {len(a)} elements")
    output = quickSelect(a.copy(), k, m)
    if output2console: print(f"quickSelect({a}, {k}, {m}) = {output}")
    if output == expectedOutput: print("Pass")
    else:
        print("Fail")
        if output2console: print(f"expected output = {expectedOutput}")
        correct = False
    print()

    return correct


if __name__ == "__main__":    
    correct = True

    a = [2, 9, 3, 0, 6, 1, 4, 5, 7, 8]
    correct = testCorrectness(a, 0, 0, [0], correct, True)
    correct = testCorrectness(a, 3, 5, [3, 4, 5], correct, True) 
    correct = testCorrectness(a, 6, 9, [6, 7, 8, 9], correct, True)
    correct = testCorrectness(a, 0, 9, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], correct, True)

    size, k, m = 100, 57, 73
    offset, step = random.randint(100, 1000), random.randint(2, 100)
    a = [offset + step*i for i in range(size)]
    random.shuffle(a)    
    expectedOutput = [offset + step*i for i in range(k, m+1)]
    correct = testCorrectness(a, k, m, expectedOutput, correct, False)

    size, k, m = 10000, 2000, 2100
    offset, step = random.randint(100, 1000), random.randint(2, 100)
    a = [offset + step*i for i in range(size)]
    random.shuffle(a)    
    expectedOutput = [offset + step*i for i in range(k, m+1)]
    correct = testCorrectness(a, k, m, expectedOutput, correct, False) 

    size, k, m, n = 100000, 20000, 20100, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements in random order")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [i for i in range(size)]        
        random.shuffle(a)
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}, which must be > 1.7")
        if tSpeedCompare / tQuickSelect > 1.7: print("Pass")
        else: print("Fail")
    print()

    size, k, m, n = 100000, 20000, 20100, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements in ascending order")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [i for i in range(size)]        
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}, which must be > 2.0")
        if tSpeedCompare / tQuickSelect > 2.0: print("Pass")
        else: print("Fail")
    print()

    size, k, m, n = 100000, 0, 100000 - 1, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements with 3 unique keys")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [random.randint(0,2) for i in range(size)]        
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n        
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}, which must be > 2.0")
        if tSpeedCompare / tQuickSelect > 2.0: print("Pass")
        else: print("Fail")
    print()
    