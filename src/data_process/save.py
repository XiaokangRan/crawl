from sklearn.utils import shuffle
import numpy as np
import pandas as pd
import pickle

def save_txt(data: list, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(data))
        f.write('\n')
        return True
    return false


# for id, row in df.itertuples():


def pd_2_csv(data: list, save_path):
    """
    :param data: list type
    :param save_path:
    :return:
    """
    pd.DataFrame(data).to_csv(save_path, encoding='utf-8')


def pd_2_excel(data: list, save_path):
    """
    :param data: list type
    :param save_path:
    :return:
    """
    pd.DataFrame(data).to_cexcel(save_path, encoding='utf-8')


def np_2_npy(data: np.array, save_path):
    """
    :param data:
    :param save_path:
    :return:
    """
    np.save(save_path, data)

savepath='./paged.bin'
paged=pickle.load(open(savepath,'rb'))   #从数据文件中读取数据，并转换为python的数据结构
paged.append(page)
pickle.dump(paged, open('paged.bin', 'wb'))   #将数据通过特殊的形式转换为只有python语言认识的字符串，并写入文件
