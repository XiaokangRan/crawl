import pickle

save_path = './save'
data = pickle.load(open(save_path,'rb'))
i = 0
j = 0
print(len(data))
if len(data) != 0:
    for x in data:
        if len(x) > 0:
            if len(x[0]) > 0:
                print(x[0][0])
            else:
                j = j + 1
        else:
            i = i + 1
print(i)
print (j)
""" 
save_path = './save_role'
data = pickle.load(open(save_path,'rb'))
print(len(data))
if len(data) != 0:
    for x in data:
        print(x[0])
"""