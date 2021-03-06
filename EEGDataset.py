import torch
import numpy as np
import scipy.sparse
from torch.utils.data import Dataset

from lib import coarsening, graph
from utils.get_data import load_data

# 跑哪个数据集
FLAG = 'small'


class EEGDataset(Dataset):

    def __init__(self, split=True, people=1):
        # (2520, 62, 5)
        super().__init__()
        self.node_num = 62

        ''' 获取数据集'''
        train_data_list, train_label_list, test_data_list, test_label_list = load_data(flag=FLAG)

        IS_TRAIN = split == True

        # train data && train label
        if IS_TRAIN:
            data = train_data_list[people]
            labels = train_label_list[people]

        # test data & test label
        else:
            data = test_data_list[people]
            labels = test_label_list[people]

        self.classes_num = 7    # 7 分类

        self.eeg_data = data
        self.eeg_labels = labels

    def __getitem__(self, idx):
        return self.eeg_data[idx], self.eeg_labels[idx]

    def __len__(self):
        return self.eeg_data.shape[0]

    @classmethod
    def build_graph(cls):

        def adjacency():
            row_ = np.array(
                [0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12,
                 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 23, 23, 24, 24, 25, 25, 26, 26,
                 27, 27, 28, 28, 29, 29, 30, 30, 31, 32, 32, 33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38, 39, 39, 40,
                 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54,
                 54, 55, 55, 56, 57, 58, 59,
                 60, 1, 3, 2, 3, 4, 4, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13, 6, 14, 7, 15, 8, 16, 9, 17, 10, 18, 11, 19, 12,
                 20, 13, 21, 22, 15, 23, 16, 24, 17, 25, 18, 26, 19, 27, 20, 28, 21, 29, 22, 30, 31, 24, 32, 25, 33, 26,
                 34, 27, 35, 28, 36, 29, 37, 30, 38, 31, 39, 40, 33, 41, 34, 42, 35, 43, 36, 44, 37, 45, 38, 46, 39, 47,
                 40, 48, 49, 42, 50, 43, 51, 44, 52, 45, 52, 46, 53, 47, 54, 48, 54, 49, 55, 56, 51, 57, 52, 57, 53, 58,
                 54, 59, 55, 60, 56, 61, 61, 58, 59, 60, 61])

            col_ = np.array(
                [1, 3, 2, 3, 4, 4, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13, 6, 14, 7, 15, 8, 16, 9, 17, 10, 18, 11, 19, 12, 20,
                 13, 21, 22, 15, 23, 16, 24, 17, 25, 18, 26, 19, 27, 20, 28, 21, 29, 22, 30, 31, 24, 32, 25, 33, 26, 34,
                 27, 35, 28, 36, 29, 37, 30, 38, 31, 39, 40, 33, 41, 34, 42, 35, 43, 36, 44, 37, 45, 38, 46, 39, 47, 40,
                 48, 49, 42, 50, 43, 51, 44, 52, 45, 52, 46, 53, 47, 54, 48, 54, 49, 55, 56, 51, 57, 52, 57, 53, 58, 54,
                 59, 55, 60, 56, 61, 61, 58,
                 59, 60, 61, 0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
                 11, 12, 12, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 23, 23, 24, 24, 25,
                 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 32, 32, 33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38,
                 39, 39, 40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 50, 50, 51, 51, 52, 52,
                 53, 53, 54, 54, 55, 55, 56, 57, 58, 59, 60])
            data_ = np.ones(236).astype('float32')
            A = scipy.sparse.csr_matrix((data_, (row_, col_)), shape=(62, 62))
            return A

        adj = adjacency()
        return adj

    @staticmethod
    def collate_fn(batch):
        data_batch = np.array([b[0] for b in batch])
        label_batch = np.array([b[1] for b in batch])
        data_batch = torch.from_numpy(data_batch).type(torch.float32)
        label_batch = torch.from_numpy(label_batch)
        return data_batch, label_batch