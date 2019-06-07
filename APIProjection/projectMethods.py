from keras.models import Sequential, load_model
from keras import backend as K
import numpy as np
from heapq import heappop, heappush
import pandas as pd
import os

K.set_image_dim_ordering('th')
model = load_model('my_model.h5')


def judge(y):
    return y[0] < y[1]


def compute_accuracy(y_true, y_pred):
    true = []
    for i in range(len(y_true)):
        true.append(judge(y_true[i]))

    res = 0
    for i in range(len(y_pred)):
        if judge(y_pred[i]) == true[i]:
            res += 1

    return res / len(y_pred)


def getSimilarAPI():
    set1 = list(open('./data/test_cs1.txt', "r", encoding='utf-8').readlines())
    set2 = list(open('./data/test_java1.txt', "r", encoding='utf-8').readlines())

    row_index = []
    similarAPI = []
    for i in set1:
        tempHeap = []
        list1 = i.split()
        row_index.append(list1[0] + '_' + list1[1])
        length_1 = int(list1[1].split('|')[0]) * 2
        input1 = np.array(list1[2:])
        input1 = input1.reshape((1, 1, 384, 1))

        for j in set2:
            list2 = j.split()
            length_2 = int(list2[1].split('|')[0])
            input2 = np.array(list2[2:])
            input2 = input2.reshape((1, 1, 384, 1))

            if length_1 * 3 > length_2 and length_2 * 3 > length_1:
                c = np.concatenate((input1, input2), axis=1)
                distance = model.predict(c)[0][1]
                col_index = list2[0] + '_' + list2[1]
                # if distance <= 0.5:
                #     distance = 0
                #     col_index = ''
                heappush(tempHeap, (distance, col_index))

        line = []
        for k in range(len(tempHeap)):
            line.insert(0, heappop(tempHeap))

        similarAPI.append(line)

    API_API = pd.DataFrame(similarAPI, index=row_index)
    API_API.to_csv('API_API.csv')


if __name__ == '__main__':
    getSimilarAPI()

# X = np.vstack((positive_examples, negative_examples))
# data_size = X.shape[0]
#
# input_1 = []
# for i in range(data_size):
#     input_1.append(X[i][:384])
# input_1 = np.array(input_1)
#
# input_2 = []
# for i in range(data_size):
#     input_2.append(X[i][384:])
# input_2 = np.array(input_2)
#
# input_1 = input_1.reshape((data_size, 1, 384, 1))
# input_2 = input_2.reshape((data_size, 1, 384, 1))
#
# c = np.concatenate((input_1, input_2), axis=1)
#
# model = load_model('my_model.h5')
# print(model.predict(c))
