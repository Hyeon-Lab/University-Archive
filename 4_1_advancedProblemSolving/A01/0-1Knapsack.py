
def ZeroOneKnapsack(n, W, items):
    weights = [items[i][1] for i in range(n)]
    profits = [items[i][2] for i in range(n)]
    
    def search(i, capacity):
        if i==n or capacity == 0:
            return 0
        else:
            max_profit = search(i + 1, capacity)
            if weights[i] <= capacity:
                max_profit = max(max_profit, profits[i] + search(i + 1, capacity - weights[i]))
        return max_profit
    
    return search(0, W)

n, W = map(int, (input().split()))
item = [[0]*3 for _ in range(n)]
for i in range(n):
    item[i][0] = i
    item[i][1], item[i][2] = map(int, (input().split()))
print(f"{ZeroOneKnapsack(n, W, item)}")
