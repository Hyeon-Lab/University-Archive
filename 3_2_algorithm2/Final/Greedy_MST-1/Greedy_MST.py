from pathlib import Path
from queue import PriorityQueue
import timeit

'''
Class for storing weighted edges
'''
class Edge:
    def __init__(self, v, w, weight): # Create an edge v-w with a double weight
        if v <= w: self.v, self.w = v, w  # Put the lesser number in v for convenience
        else: self.v, self.w = w, v        
        self.weight = weight
    
    def __lt__(self, other): # < operator, used to sort elements (e.g., in a PriorityQueue, sorted() function)
        assert(isinstance(other, Edge))
        return self.weight < other.weight

    def __gt__(self, other): # > operator, used to sort elements
        assert(isinstance(other, Edge))
        return self.weight > other.weight

    def __eq__(self, other): # == operator, used to compare edges for grading
        assert(isinstance(other, Edge))
        return self.v == other.v and self.w == other.w and self.weight == other.weight

    def __str__(self): # Called when an Edge instance is printed (e.g., print(e))
        return f"Edge({self.v}, {self.w}, {self.weight})"
        #return f"{self.v}-{self.w} ({self.weight})"

    def __repr__(self): # Called when an Edge instance is printed as an element of a list
        return self.__str__()

    def other(self, v): # Return the vertex on the Edge other than v
        if self.v == v: return self.w
        else: return self.v

'''
Class for storing WUGraphs (Weighted Undirected Graphs)
'''
class WUGraph:
    def __init__(self, V): # Constructor
        self.V = V # Number of vertices
        self.E = 0 # Number of edges
        self.adj = [[] for _ in range(V)]   # adj[v] is a list of vertices adjacent to v
        self.edges = []

    def addEdge(self, v, w, weight): # Add edge v-w. Self-loops and parallel edges are allowed
        e = Edge(v, w, weight) # Create one edge instance and use it for adj[v], adj[w], and edges[]
        self.adj[v].append(e)
        self.adj[w].append(e)
        self.edges.append(e)
        self.E += 1

    def degree(self, v):
        return len(self.adj[v])

    def __str__(self):
        rtList = [f"{self.V} vertices and {self.E} edges\n"]
        for v in range(self.V):
            for e in self.adj[v]:
                if v == e.v: rtList.append(f"{e}\n") # Do not print the same edge twice
        return "".join(rtList)

    '''
    Create a WUGraph instance from a file
        fileName: Name of the file that contains graph information as follows:
            (1) the number of vertices, followed by
            (2) one edge in each line, where an edge v-w with weight is represented by "v w weight"
            e.g., the following file represents a digraph with 3 vertices and 2 edges
            3
            0 1 0.12
            2 0 0.26
        The file needs to be in the same directory as the current .py file
    '''
    @staticmethod
    def fromFile(fileName):
        filePath = Path(__file__).with_name(fileName)   # Use the location of the current .py file   
        with filePath.open('r') as f:
            phase = 0
            line = f.readline().strip() # Read a line, while removing preceding and trailing whitespaces
            while line:                                
                if len(line) > 0:
                    if phase == 0: # Read V, the number of vertices
                        g = WUGraph(int(line))
                        phase = 1
                    elif phase == 1: # Read edges
                        edge = line.split()
                        if len(edge) != 3: raise Exception(f"Invalid edge format found in {line}")
                        g.addEdge(int(edge[0]), int(edge[1]), float(edge[2]))                        
                line = f.readline().strip()
        return g

'''
Class for performing Union Find using weighted quick union
    and storing the results    
'''
class UF:
    def __init__(self, V): # V: the number of vertices
        self.ids = [] # ids[i]: i's parent
        self.size = [] # size[i]: size of tree rooted at i
        for idx in range(V):
            self.ids.append(idx)
            self.size.append(1)       

    def root(self, i):
        while i != self.ids[i]: i = self.ids[i]
        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        id1, id2 = self.root(p), self.root(q)
        if id1 == id2: return
        
        if self.size[id1] < self.size[id2]: id1, id2 = id2, id1 # Size가 큰 쪽이 id1이 되도록 하고
        elif self.size[id1] == self.size[id2]:                  # Size가 같다면 더 작은 id가 id1이 되도록 함
            if id2 < id1: id1, id2 = id2, id1               

        self.ids[id2] = id1
        self.size[id1] += self.size[id2]

'''
Min Priority Queue based on a binary heap 
    with decreaseKey operation added
'''
class IndexMinPQ:
    def __init__(self, maxN): # Create an indexed PQ with indices 0 to (N-1)
        if maxN < 0: raise Exception("maxN < 0")
        self.maxN = maxN # Max number of elements on PQ
        self.n = 0 # Number of elements on PQ
        self.keys = [None] * (maxN+1)  # keys[i]: key with index i
        self.pq = [-1] * (maxN+1)  # pq[i]: index of the key at heap position i (pq[0] is not used)        
        self.qp = [-1] * maxN # qp[i]: heap position of the key with index i (inverse of pq[])        

    def isEmpty(self):
        return self.n == 0

    def contains(self, i): # Is i an index on the PQ?
        self.validateIndex(i)
        return self.qp[i] != -1

    def size(self):
        return self.n

    def insert(self, i, key): # Associate key with index i
        self.validateIndex(i)
        if self.contains(i): raise Exception(f"index {i} is already in PQ")
        self.n += 1
        self.qp[i] = self.n
        self.pq[self.n] = i
        self.keys[i] = key
        self.swimUp(self.n)

    def minIndex(self): # Index associated with the minimum key
        if self.n == 0: raise Exception("PQ has no element, so no min index exists")
        return self.pq[1]

    def minKey(self):
        if self.n == 0: raise Exception("PQ has no element, so no min key exists")
        return self.keys[self.pq[1]]

    def delMin(self):
        if self.n == 0: raise Exception("PQ has no element, so no element to delete")
        minIndex = self.pq[1]
        minKey = self.keys[minIndex]
        self.exch(1, self.n)
        self.n -= 1
        self.sink(1)
        assert(minIndex == self.pq[self.n+1])
        self.qp[minIndex] = -1 # Mark the index as being deleted
        self.keys[minIndex] = None
        self.pq[self.n+1] = -1
        return minKey, minIndex

    def keyOf(self, i):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        else: return self.keys[i]

    def changeKey(self, i, key):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        self.keys[i] = key
        self.swimUp(self.qp[i])
        self.sink(self.qp[i])

    def decreaseKey(self, i, key):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        if self.keys[i] == key: raise Exception(f"calling decreaseKey() with key {key} equal to the previous key")
        if self.keys[i] < key: raise Exception(f"calling decreaseKey() with key {key} greater than the previous key {self.keys[i]}")
        self.keys[i] = key
        self.swimUp(self.qp[i])

    def increaseKey(self, i, key):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        if self.keys[i] == key: raise Exception(f"calling increaseKey() with key {key} equal to the previous key")
        if self.keys[i] > key: raise Exception(f"calling increaseKey() with key {key} smaller than the previous key {self.keys[i]}")
        self.keys[i] = key
        self.sink(self.qp[i])

    def delete(self, i):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        idx = self.qp[i]
        self.exch(idx, self.n)
        self.n -= 1
        self.swimUp(idx)
        self.sink(idx)
        self.keys[i] = None
        self.qp[i] = -1   

    def validateIndex(self, i):
        if i < 0: raise Exception(f"index {i} < 0")
        if i >= self.maxN: raise Exception(f"index {i} >= capacity {self.maxN}")

    def greater(self, i, j):
        return self.keys[self.pq[i]] > self.keys[self.pq[j]]

    def exch(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def swimUp(self, idx): # idx is the index in pq[]
        while idx>1 and self.greater(idx//2, idx):
            self.exch(idx, idx//2)            
            idx = idx//2

    def sink(self, idx): # idx is the index in pq[]
        while 2*idx <= self.n:    # If a child exists
            idxChild = 2*idx # Left child
            if idxChild<self.n and self.greater(idxChild, idxChild+1): idxChild = idxChild+1 # Find the smaller child
            if not self.greater(idx, idxChild): break
            self.exch(idx, idxChild) # Swap with (i.e., sink to) the greater child
            idx = idxChild


'''
Find an MST (Minimum Spanning Tree)
    and return the MST with its weight sum
'''
def mst2025_basic(g):
    
    cc = UF(g.V)
    connected_edge_list = []
    total_weight = 0
    pq = []
    #print(g)
    for v in range(g.V):
        #print(v, g.degree(v))
        pq.append(IndexMinPQ(g.V))
        for e in g.adj[v]:
            #print("!",e.other(v), e)
            if(pq[v].contains(e.other(v))):
                if(pq[v].keyOf(e.other(v)) > e):
                    pq[v].decreaseKey(e.other(v), e)
            else:
                pq[v].insert(e.other(v), e)

    while(len(connected_edge_list) < g.V-1):

        min_cc = cc.size[cc.root(0)]
        min_cc_root = cc.root(0)

        #size가 가장 작은 cc구함
        for i in range(len(cc.size)):
            if(cc.size[cc.root(i)] < min_cc):
                min_cc = cc.size[cc.root(i)]
                min_cc_root = cc.root(i)
        #print("!!!!!!min_cc", min_cc, min_cc_root)
    
        #가장 작은 컴포넌트에서 min weight edge 구함
        if(pq[min_cc_root].n != 0):
            min_v, min_edge_index, min_edge = min_cc_root, pq[min_cc_root].minIndex(), pq[min_cc_root].minKey()
        else:
            min_edge = Edge(-1, -1, float('inf'))
        for v in range(g.V):
            if(pq[v].n != 0):
                if(cc.connected(v, min_cc_root) and min_edge > pq[v].minKey()):
                    min_v, min_edge_index, min_edge = v, pq[v].minIndex(), pq[v].minKey()
        
        pq[min_v].delMin()
        connected_edge_list.append(min_edge)
        total_weight += min_edge.weight

        #작은 컴포넌트와 union
        cc.union(min_edge_index, min_cc_root)

        #컴포넌트내 edge minPQ에서 제외
        for v in range(g.V):
            if(cc.connected(v, min_cc_root)):
                # print("v", v)
                # print("pq[v].contains(min_edge_index)", pq[v].contains(min_edge_index))
                # print("pq[min_edge_index].contains(v)", pq[min_edge_index].contains(v))
                if(pq[v].contains(min_edge_index)):
                    pq[v].delete(min_edge_index)
                elif(pq[min_edge_index].contains(v)):
                    pq[min_edge_index].delete(v)

    return connected_edge_list, total_weight


def grade(g_num, sum, e_list, failCorrectness):
    g = WUGraph.fromFile(f"wugraph{g_num}.txt")
    print(f"results on g{g_num}")    
    edges, weightSum = mst2025_basic(g)
    if e_list is not None:        
        print(f"mst2025_basic:", (edges, weightSum))        
        if edges == e_list and weightSum == sum: print ("pass")
        else: 
            print (f"fail, expected results: {(e_list, sum)}")
            failCorrectness = True
    else:
        print(f"mst2025_basic:", weightSum)        
        if weightSum == sum: print ("pass")
        else: 
            print (f"fail, expected sum: {sum}")        
            failCorrectness = True
    print()
    return failCorrectness


if __name__ == "__main__":
    failCorrectness = False
    failCorrectness = grade("3", 11, [Edge(0, 1, 4), Edge(1, 2, 7)], failCorrectness)
    failCorrectness = grade("4", 10, [Edge(0, 3, 2.0), Edge(0, 1, 3.0), Edge(0, 2, 5.0)], failCorrectness)
    failCorrectness = grade("5", 10, [Edge(0, 3, 1.0), Edge(1, 4, 3.0), Edge(2, 4, 2.0), Edge(3, 4, 4.0)], failCorrectness)
    failCorrectness = grade("8a", 50, [Edge(0, 1, 5.0), Edge(2, 3, 4.0), Edge(1, 4, 8.0), Edge(5, 6, 7.0), Edge(5, 7, 9.0), Edge(1, 2, 6.0), Edge(0, 5, 11.0)], failCorrectness)
    failCorrectness = grade("8", 1.81, [Edge(0, 7, 0.16), Edge(1, 7, 0.19), Edge(2, 3, 0.17), Edge(4, 5, 0.35), Edge(2, 6, 0.4), Edge(5, 7, 0.28), Edge(0, 2, 0.26)], failCorrectness)
    failCorrectness = grade("10", 4.34, [Edge(0, 6, 0.39), Edge(1, 2, 0.08), Edge(3, 9, 0.17), Edge(3, 4, 0.68), Edge(1, 5, 0.48), Edge(3, 7, 0.38), Edge(3, 8, 0.96), Edge(0, 7, 0.73), Edge(1, 9, 0.47)], failCorrectness)
    failCorrectness = grade("50", 82124, None, failCorrectness)
    failCorrectness = grade("500", 83208749, None, failCorrectness)
   
    if failCorrectness: print("fail - since the algorithm is not correct")
    else:        
        n, mult = 3, 200
        g1, g2 = WUGraph.fromFile(f"wugraph50.txt"), WUGraph.fromFile(f"wugraph500.txt")
        tMST2025_50 = timeit.timeit(lambda: mst2025_basic(g1), number=n)/n        
        tMST2025_500 = timeit.timeit(lambda: mst2025_basic(g2), number=n)/n
        print(f"Average running time for g50*{mult} and g500: {tMST2025_50 * mult}, {tMST2025_500}")
        if tMST2025_500 < tMST2025_50 * mult: print("pass")
        else: print("fail")
    print()