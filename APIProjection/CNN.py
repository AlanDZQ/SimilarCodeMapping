from keras.models import Sequential, load_model
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
import numpy as np

K.set_image_dim_ordering('th')


def judge(y):
    return y[0] < y[1]


def compute_accuracy(y_true, y_pred):
    true = []
    for i in range(len(y_true)):
        true.append(judge(y_true[i]))

    res = 0
    for i in range(len(y_pred)):
        if judge(y_pred[i])==true[i]:
            res += 1

    return res/len(y_pred)


# import your data here instead
# X - inputs, 10000 samples of 128-dimensional vectors
# y - labels, 10000 samples of scalars from the set {0, 1, 2}

# positive_examples = np.loadtxt('./data/rt-polaritydata/train_true.txt')
# negative_examples = np.loadtxt('./data/rt-polaritydata/train_false.txt')
# P = np.vstack((positive_examples, negative_examples))
# data_size = P.shape[0]
#
# X = []
# for i in range(data_size):
#     X.append(P[i].reshape(2, -1))
# X = np.array(X)
#
# positive_labels = [[0, 1] for _ in positive_examples]
# negative_labels = [[1, 0] for _ in negative_examples]
# y = np.concatenate([positive_labels, negative_labels], 0)
#
# # X = np.random.rand(1000, 768).astype("float32")
# # y = np.random.randint(2, size=(1000, 1))
#
# # output labels should be one-hot vectors - ie,
# # 0 -> [0, 0, 1]
# # 1 -> [0, 1, 0]
# # 2 -> [1, 0, 0]
# # this operation changes the shape of y from (10000,1) to (10000, 3)
#
# # y = np_utils.to_categorical(y)
#
#
# # Randomly shuffle data
# np.random.seed(10)
# shuffle_indices = np.random.permutation(np.arange(len(y)))
# X = X[shuffle_indices]
# y = y[shuffle_indices]
#
# # process the data to fit in a keras CNN properly
# # input data needs to be (N, C, X, Y) - shaped where
# # N - number of samples
# # C - number of channels per sample
# # (X, Y) - sample size
#
# X = X.reshape((data_size, 1, 768, 1))


positive_examples = np.loadtxt('./data/rt-polaritydata/Test_Pos.txt')
negative_examples = np.loadtxt('./data/rt-polaritydata/Test_Neg.txt')
X = np.vstack((positive_examples, negative_examples))
data_size = X.shape[0]

input_1 = []
for i in range(data_size):
    input_1.append(X[i][:384])
input_1 = np.array(input_1)

input_2 = []
for i in range(data_size):
    input_2.append(X[i][384:])
input_2 = np.array(input_2)

positive_labels = [[0, 1] for _ in positive_examples]
negative_labels = [[1, 0] for _ in negative_examples]
y = np.concatenate([positive_labels, negative_labels], 0)

np.random.seed(10)
shuffle_indices = np.random.permutation(np.arange(len(y)))
input_1 = input_1[shuffle_indices]
input_2 = input_2[shuffle_indices]
y_train = y[shuffle_indices]

input_1 = input_1.reshape((data_size, 1, 384, 1))
input_2 = input_2.reshape((data_size, 1, 384, 1))

c = np.concatenate((input_1, input_2), axis=1)

# define a CNN
# see http://keras.io for API reference

# cnn = Sequential()
# cnn.add(Conv2D(64, 3, 1, border_mode="same", activation="relu", input_shape=(2, 384, 1)))
# cnn.add(Conv2D(64, 3, 1, border_mode="same", activation="relu"))
# cnn.add(MaxPooling2D(pool_size=(2, 1)))
#
# cnn.add(Conv2D(128, 3, 1, border_mode="same", activation="relu"))
# cnn.add(Conv2D(128, 3, 1, border_mode="same", activation="relu"))
# cnn.add(Conv2D(128, 3, 1, border_mode="same", activation="relu"))
# cnn.add(MaxPooling2D(pool_size=(2, 1)))
#
# cnn.add(Conv2D(256, 3, 1, border_mode="same", activation="relu"))
# cnn.add(Conv2D(256, 3, 1, border_mode="same", activation="relu"))
# cnn.add(Conv2D(256, 3, 1, border_mode="same", activation="relu"))
# cnn.add(MaxPooling2D(pool_size=(2, 1)))
#
# cnn.add(Flatten())
# cnn.add(Dense(1024, activation="relu"))
# cnn.add(Dropout(0.5))
# cnn.add(Dense(2, activation="softmax"))
# plot_model(cnn, to_file='model_test.png',show_shapes=True)


# # define optimizer and objective, compile cnn
#
# cnn.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
#
# # train
#
# cnn.fit(c, y_train, epochs=10)
#
# cnn.save('my_model.h5')

model = load_model('my_model.h5')

tr_acc = compute_accuracy(y_train, model.predict(c))
print(tr_acc)
