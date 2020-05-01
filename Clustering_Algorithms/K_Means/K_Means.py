import math
N, k = input().split(" ")
N = int(N)
k = int(k)
points = []
while True:
    try:
        point = input().split(" ")[0:-1]
        point = [float(i) for i in point]
        points.append(point)
    except EOFError:
        break

centroids = tuple(points[-k:])
points = points[:-k]
D = len(points[0])

for center in centroids:
    center = tuple(center)
# Euclidean distance between any points in any dimension
def Euclidean(point, centroid):
    res = 0
    for i in range(D):
        res += pow((float(point[i]) - float(centroid[i])), 2)
    return math.sqrt(res)

while True:
    cluster = {}
    for center in centroids:
        cluster[tuple(center)] = []
    for point in points:
        min_dis = float("inf")
        closed_center = []
        for center in centroids:
            curr = Euclidean(point, center)
            if curr < min_dis:
                min_dis = curr
                closed_center = tuple(center)
        cluster[closed_center].append(point)
    new_centroid = []
    
    for center, items in cluster.items():
        sum_point = [sum(x) for x in zip(*items)]
        new_center = [x / len(items) for x in sum_point]    
        new_centroid.append(new_center)    
    res = 0

    for i in range(len(new_centroid)):
        res += Euclidean(new_centroid[i], centroids[i])
    centroids = new_centroid
    if res <= 1e-5:
        break

for point in points:
    for i in range(len(centroids)):
        cen = centroids[i]
        if point in cluster[tuple(cen)]:
            print(i)