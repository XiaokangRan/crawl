from sklearn.utils import shuffle
import numpy as np
import pandas as pd


def save_txt(file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(file_path))
        f.write('\n')
        return True
    return false





