
def fractionalKnapsack(n, W, items):
    items.sort(key=lambda x: x[2] / x[1], reverse = True)
    weights = [items[i][1] for i in range(n)]
    profits = [items[i][2] for i in range(n)]
    picks = []
    capacity = W
    for i in range(n):
        if weights[i] <= capacity:
            picks.append(1.0)
            capacity -= weights[i]
        else:
            picks.append(capacity/weights[i])
            capacity = 0
            break
    total_profit = sum(profits[i] * picks[i] for i in range(len(picks)))
    return total_profit

n, W = map(int, (input().split()))
item = [[0]*3 for _ in range(n)]
for i in range(n):
    item[i][0] = i
    item[i][1], item[i][2] = map(int, (input().split()))
print(f"{fractionalKnapsack(n, W, item):.2f}")
