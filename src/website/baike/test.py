import pickle

save_path = './save'
data = pickle.load(open(save_path,'rb'))
print(len(data))
if len(data) != 0:
    for x in data:
        print(x[0])

save_path = './save_role'
data = pickle.load(open(save_path,'rb'))
print(len(data))
if len(data) != 0:
    for x in data:
        print(x[0][0])
