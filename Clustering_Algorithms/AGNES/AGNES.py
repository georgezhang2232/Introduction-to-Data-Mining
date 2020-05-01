import math
N, K = input().split(" ")
N = int(N)
K = int(K)
points = []
while True:
    try:
        point = input().split(" ")[:-1]
        point = [float(i) for i in point]
        points.append(point)
    except EOFError:
        break
D = len(points[0])
def Euclidean(point1, point2):
    res = 0
    for i in range(D):
        res += pow((point1[i] - point2[i]), 2)
    return math.sqrt(res)
dis = [0 for i in range(N)]
for index, point in enumerate(points):
    dis[index] = [0 for i in range(N)]
    for j in range(N):
        if j == index:
            dis[index][j] = float("inf")
        else:
            distance = Euclidean(point, points[j])
            dis[index][j] = distance
flat_dis = []
for index, row in enumerate(dis):
    for index2, col in enumerate(row):
        flat_dis.append([col, (index, index2)])
candidate = sorted(flat_dis, key=lambda x: (x[0], min(x[1][0], x[1][1]), max(x[1][0], x[1][1])))
candidate = [x[1] for x in candidate[::2]]
cluster = [{0.1}]
for pair in candidate:
    for i in range(len(cluster)):
        if (pair[0] in cluster[i]) or (pair[1] in cluster[i]):
            cluster[i].add(pair[0])
            cluster[i].add(pair[1])
            break
        if i == len(cluster) - 1:
            cluster.append({pair[0], pair[1]})
    for j in range(len(cluster)):
        for k in range(j+1, len(cluster)):
            if not cluster[j].isdisjoint(cluster[k]):
                cluster[j] = cluster[j].union(cluster[k])
                cluster[k] = {0.1}
    cluster = [x for x in cluster if x != {0.1}]
    sum = 0
    for each_set in cluster:
        sum += len(each_set)
    if len(cluster) == K and sum == N:
        break

for i in range(N):
    for j in range(K):
        if i in cluster[j]:
            print(min(cluster[j]))