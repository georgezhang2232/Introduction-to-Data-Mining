import itertools
from collections import Counter
min_sup=int(input())
db = []
comb = []
while True:
    try:
        sentence = input()
    except EOFError:
        break
    db.append(sentence.split())
# db is [['B', 'A', 'C', 'E', 'D'], ['A', 'C'], ['C', 'B', 'D']]
# find max combinations length
maxlen = 0
for transition in db:
    if len(transition) > maxlen:
        maxlen = len(transition)      
for item in db:
    for i in range(maxlen):
        c = [list(l) for l in itertools.combinations(item, i)]
        comb.extend(c)         
# sort, join and deliminate empty
sort_list=[sorted(i) for i in comb]
seperator = ' '
join_list=[seperator.join(x) for x in sort_list]
done_list=[i for i in join_list if i != ""]
#count itemset and deliminate infrequent itemset
cnt = Counter(done_list)
infrequent = [key for key in cnt if cnt[key] < min_sup]
for key in infrequent: del cnt[key]
count_list = cnt.items()
# desc by support, ascd by alphabetic
# [('C', 3), ('A', 2), ('A C', 2), ('B', 2), ('B C', 2), ('B C D', 2), ('B D', 2), ('C D', 2), ('D', 2)]
frequent_list = sorted(count_list, key=lambda support: (-support[1], support[0]))
# output frequent itemsets
for i in frequent_list:
    print(i[1],"["+i[0]+"]")
print("")

# FIND CLOSED PATTERNS
closed = []
frelen = len(frequent_list)
for temp1 in frequent_list:
    flag = 0
    for temp2 in frequent_list:
        if temp1 != temp2 and set(temp1[0]).issubset(set(temp2[0])) and temp1[1] <= temp2[1]:
            flag = 1
            break
    if flag == 0:
        closed.append(temp1)
closed = sorted(closed, key=lambda support: (-support[1], support[0]))      
for i in closed:
    print(i[1],"["+i[0]+"]")
print("")


# FIND MAX-PATTERN
max_pattern = []
for temp1 in frequent_list:
    flag = 0
    for temp2 in frequent_list:
        if temp1 != temp2 and set(temp1[0]).issubset(set(temp2[0])):
            flag = 1
            break
    if flag == 0:
        max_pattern.append(temp1)
max_pattern = sorted(max_pattern, key=lambda support: (-support[1], support[0]))      
for i in max_pattern:
    print(i[1],"["+i[0]+"]")
print("")