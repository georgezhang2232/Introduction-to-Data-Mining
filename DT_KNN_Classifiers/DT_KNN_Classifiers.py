import math
from collections import Counter 

train_data = {}  # key = index, value = [label] [attribute 1]:[value 1] [attribute 2]:[value 2] ..
test_data = [] 
i = 0
while True:
    try:
        s=input().split(" ")
        if (s[0] != "0"): 
            train_data[i] = s
            i += 1
        else :
            test_data.append(s)         
    except EOFError:
        break

num_atts = len(train_data[0]) - 1       

######################### KNN Classifiers #######################

def KNN(train, test) :
    neighbors = {} ## key:index of train, value: distance
    predict = []
    for index, test_v in enumerate(test) :
        for train_k, train_v in train.items() :
            euclidean  = 0
            for i in range(1, num_atts+1) :
                test_value = float(test_v[i].split(":")[1])
                train_value = float(train_v[i].split(":")[1])
                euclidean += (test_value - train_value) ** 2
            neighbors[train_k] = math.sqrt(euclidean) # euclidean distance for test and train data 
    
        nearest_3_neighbor = sorted(neighbors.items(), key=lambda x:(x[1],x[0]))[0:3]
        vote = Counter()
        for item in nearest_3_neighbor:
            label = train[item[0]][0]
            vote.update(label)
        res = sorted(vote.items(), key=lambda x:(-x[1],x[0]))[0][0]
        predict.append(res)
    return predict


########################### DT Classifiers########################


# Given a dataset, return a Counter containing counts of each label in this dataset
def get_labels(data) :
    labels = Counter() 
    for k,v in data.items() :
        labels.update(v[0])
    return labels 

# Given index of attribute value that less than split point and larger than split point, return the gini index
def gini(left, right):
    left_len = len(left)
    right_len = len(right)
    left_coef = float( left_len /(left_len + right_len))
    right_coef = 1 - left_coef                     
    left_gini = 1
    right_gini = 1 
                      
    left_labels = {}
    for i in left:
        label = train_data[i][0] 
        if label not in left_labels: 
            left_labels[label] = 1
        else: 
            left_labels[label] += 1
    for k,v in left_labels.items() :
        left_gini -= ((float(v) / left_len) ** 2)
                      
    right_labels = {}
    for i in right:
        label = train_data[i][0] 
        if label not in right_labels: 
            right_labels[label] = 1
        else: 
            right_labels[label] += 1
    for k,v in right_labels.items() :
        right_gini -=  ((float(v) / right_len) ** 2)

    return (left_coef * left_gini + right_coef * right_gini)

# Given data set, return the attribute and its value to split, and left child and right child data after split
def DT(data) :
        candidate = {} # all candidate 
        ## for each attribute find the distinct value and the midpoint for possible split point
        for i in range(1, num_atts+1) :
            attr_idx = {}
            attr_val = []
            for k,v in data.items() :
                a = float(v[i].split(":")[1])
                attr_idx[k] = a
                attr_val.append(a)
            distinct_list = list(set(attr_val))
            distinct_val = sorted(distinct_list)
            
            split = [] 
            for j in range(len(distinct_val) - 1):
                mid_point = float(distinct_val[j] + distinct_val[j+1])/2
                split.append(mid_point)
                               
            ## find the split point with the min gini index, add to candidate dict
            min_gini = float("inf")
            threshold = float("inf")
            min_left = []
            min_right = []
            for split_point in split:
                left_idx = [] #index of value less than split_point
                right_idx = []  #index of value greater than split_point
                for k, v in attr_idx.items():
                    if v < split_point:
                        left_idx.append(k)
                    else:
                        right_idx.append(k)
                gini_ = gini(left_idx, right_idx)
                if gini_ < min_gini :
                    min_gini = gini_
                    threshold = split_point
                    min_left = left_idx
                    min_right = right_idx
            candidate[i] = [min_gini, threshold, min_left, min_right]
        
        attr = sorted(candidate.items(), key=lambda x:(x[1][0],x[0]))[0][0]  # attribute with min gini_index for split
        threshold = candidate[attr][1] # value of split point
        left_data = {} # left child data set 
        right_data = {}  # right child data set
        for index in candidate[attr][2]:
            left_data[index] = data[index] 
        for index in candidate[attr][3]:
            right_data[index] = data[index] 
            
        return (attr, threshold, left_data, right_data)


# build the division tree with max depth = 2

model = [] # model[0] = 1st split, model[1] = 2nd split for left child, mode1[3] = 2nd split for right child
level_1 = DT(train_data)
model.append(level_1)
left_2 = DT(level_1[2])
right_2 = DT(level_1[3])
model.append(left_2)
model.append(right_2)


# predict label for test data

predict = []
for v in test_data:
    attr_idx= model[0][0]
    threshold = model[0][1]

    value = float(v[attr_idx].split(":")[1])
    
    # go right child
    if value > threshold:
        attr_idx = model[2][0]
        threshold = model[2][1]
        value = float(v[attr_idx].split(":")[1])
        # go right child
        if value > threshold:
            labels = get_labels(model[2][3])
            label = labels.most_common(1)[0][0]
            predict.append(label)
        # go left child    
        else:
            labels = get_labels(model[2][2])
            label = labels.most_common(1)[0][0]
            predict.append(label)

    # go left child
    else:
        attr_idx = model[1][0]
        threshold = model[1][1]
        value = float(v[attr_idx].split(":")[1])
        # go right child
        if value > threshold:
            labels = get_labels(model[1][3])
            label = labels.most_common(1)[0][0]
            predict.append(label)
        # go left child    
        else:
            labels = get_labels(model[1][2])
            label = labels.most_common(1)[0][0]
            predict.append(label)

            
# print DT result
for label in predict:
    print(label)
print()

#print KNN result
predict = KNN(train_data, test_data)
for label in predict:
    print(label)
