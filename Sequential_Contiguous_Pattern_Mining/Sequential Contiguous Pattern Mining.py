doc = []
db = {}
min_sup = 2

while True:
    try:
        s=input()
        doc.append(s.split( " "))
    except EOFError:
        break

for i in range(len(doc)) :
    for j in range(len(doc[i])) :
        word = doc[i][j]
        pos = (i, j)
        if word not in db:
            db[word]=[pos]
        else:
            db[word].append(pos)
            
new_db = {}
for word, pos in db.items():
    if len(pos) >= min_sup:
        new_db[word] = pos

count_db = {}     
for i in range(2,6):
    candidate = {}
    for word, pos in new_db.items():
        for temp_pos in pos:
            x, y = temp_pos
            sentence = doc[x]
            if y < len(sentence) - 1:
                temp = ' '.join([word, sentence[y+1]])
                if temp not in candidate:
                    candidate[temp] = [(x, y + 1)]
                else:
                    candidate[temp].append((x, y + 1))
    frequent = {}
    for word, pos in candidate.items():
        if len(pos) >= min_sup:
            frequent[word] = pos
    for item in frequent:
        count_db[item] = len(frequent[item])
    new_db = frequent.copy()
    
sortdict = sorted(count_db.items(), key=lambda word:(-word[1],word[0]))
sorted_list = []
for item in sortdict:
    sorted_list.append(item[0])
sorted_list = sorted_list[:20]
for item in sorted_list:
    print("[" + str(count_db[item]) + ", " + "'" + item + "'" +"]")