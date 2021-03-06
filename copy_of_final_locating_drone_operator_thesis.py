# -*- coding: utf-8 -*-
"""Copy of Final_locating_drone_operator_thesis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yuymFhepmDckND-g776BvgoPO8jimi6e

## Imports
"""
from __future__ import absolute_import, division, unicode_literals

import os
import csv
from random import random

import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split

print("TensorFlow version: {}".format(tf.__version__)) # TensorFlow version: 2.3.0
print("Eager execution: {}".format(tf.executing_eagerly()))

"""## Variables and configs"""

Sequential = tf.keras.Sequential
Dense = tf.keras.layers.Dense
LSTM = tf.keras.layers.LSTM
GRU = tf.keras.layers.GRU

#
DS_FOLDER = "./data"
# CURR_FOLDER = "/content/"
# ZIPPED_DS_FILE_PATH = CURR_FOLDER + "DS.zip"
# # CLASS_NAMES = ['FPV', 'north_west_tree', 'south_east_biob', 'stop_signpost']
CLASS_NAMES = ['FPV', 'north_west_tree', 'south_east_sewer', 'stop_signpost']
#
# TXT_FILE_EXTENTION = ".txt"
# TRAIN_FILE_EXTENTION = TXT_FILE_EXTENTION
# TEST_FILE_EXTENTION = ".test"
#
TRAIN_DATASET_FILE_NAME = "training.csv"
TEST_DATASET_FILE_NAME = "test.csv"
#
TRAIN_DATASET_FILE_PATH = DS_FOLDER + TRAIN_DATASET_FILE_NAME
TEST_DATASET_FILE_PATH = DS_FOLDER + TEST_DATASET_FILE_NAME
#
# my_zipped_records_url = "https://drive.google.com/uc?id=10bfKtAgR1MNqsgM5LJbPz2j_uJ8NHmfU"
#
# my_full_AB_zipped_records_url = "https://drive.google.com/uc?id=1XqCt3v1SmQDZW8yDTZMfOGEGS40yX0rq"
# my_full_ABC_zipped_records_url = "https://drive.google.com/uc?id=1yOGgzR97BqS-dgXIkp3o9BFE8tG0TgOw"
#
#
# zipped_small_random_records_url = "https://drive.google.com/uc?id=1a-ggoDC34RVBPNDd0DTxmw-4ytvw2BKO"
# zipped_random_records_url = "https://drive.google.com/uc?id=1C3pKRDifsYxWlMSveKl8KkL8jN8Zyqny"
# zipped_const012_records_url = "https://drive.google.com/uc?id=1bqaNDNyWs9FCtPdPdnDbsK6lSYpuAzGh"
#
# zipped_records_url = my_full_ABC_zipped_records_url

_NUMBER_OF_POINTS = 120
NUMBER_OF_VECTORES = 3 # vectore can be "x", "y", "z", "r" (row), "p" (pitch), "y" can also be 7 or 4

NUMBER_OF_FEATURES = _NUMBER_OF_POINTS * NUMBER_OF_VECTORES   # Sould be multiple of 3 (x, y, z)

# column order in the Data Set (+ the lable point_of_view)
if NUMBER_OF_VECTORES == 3:
  _FIREST_COLUMNS_NAMES = [['X_{}'.format(i), 'Y_{}'.format(i), 'Z_{}'.format(i)] for i in range(int(NUMBER_OF_FEATURES / NUMBER_OF_VECTORES))]
if NUMBER_OF_VECTORES == 4:
  _FIREST_COLUMNS_NAMES = [['QW_{}'.format(i), 'QX_{}'.format(i), 'QY_{}'.format(i), 'QZ_{}'.format(i)] for i in range(int(NUMBER_OF_FEATURES / NUMBER_OF_VECTORES))]
if NUMBER_OF_VECTORES == 7:
  _FIREST_COLUMNS_NAMES = [['X_{}'.format(i), 'Y_{}'.format(i), 'Z_{}'.format(i),'QW_{}'.format(i), 'QX_{}'.format(i), 'QY_{}'.format(i), 'QZ_{}'.format(i)] for i in range(int(NUMBER_OF_FEATURES / NUMBER_OF_VECTORES))]

# Flatening the list of list
_FEATURES_NAMES = [item for sublist in _FIREST_COLUMNS_NAMES for item in sublist]

# LABEL_NAME is the prediction field
LABEL_NAME = "point_of_view"
COLUMNS_NAMES = _FEATURES_NAMES + [LABEL_NAME]

print("Features: {}".format(_FEATURES_NAMES))
print("columns : {}".format(COLUMNS_NAMES))
print("Label   : {}".format(LABEL_NAME))
# OUTPUT:
# Features: ['X_0', 'Y_0', 'Z_0', 'X_1', 'Y_1', 'Z_1',..., 'X_119', 'Y_119', 'Z_119']
# columns: ['X_0', 'Y_0', 'Z_0', 'X_1', 'Y_1', 'Z_1',..., 'X_119', 'Y_119', 'Z_119', point_of_view]
# Label   : point_of_view

"""
    Helper functions
"""


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def feature_padding(features, padd_size):
    """
    Add padding to features - the function add the last x, y, z values to the end of the list - until we got to padd_size
    :param features:
    :param padd_size: number of features (120*(x,y,z))
    :return:
    """
    if len(features) < 3:
        print(features)
        raise Exception("feature_padding: features length is too small")

    for i in range(padd_size):
        features += [features[-3]]
    return features


def fix_features_size(features, size):
    """
    Get list of features and size and return a list of the features with length of `size` (by cut \ padd)
    :param features:
    :param size: number of features (120*(x,y,z))
    :return:
    """
    features = features[:size]
    if len(features) < size:
        features = feature_padding(features, size - len(features))
    return features


def save_list_to_CSV(data, file_path):
    """
    Write the `data` to csv file in `file_path`
    :param data: list of lists
    :param file_path: location of the csv file
    :return:
    """
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


div_num = 20  # normalize the number to be < 1


def create_data_set(files_names):
    """
    reading the txt file and parsing it into excel, and normalizing
    :param files_names: list of files names
    :return:
    """
    all_data = []
    for filename in files_names:
        data = []
        save_data = False
        with open(os.path.join(root, filename)) as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                x_val = splited_line[1]
                if (isfloat(x_val) and float(x_val) != 0.0):
                    save_data = True
                if (save_data):
                    xyz_data = [str(float(x) / div_num) for x in splited_line[1:NUMBER_OF_VECTORES + 1]]
                    data += xyz_data  # splited_line[1:4]
        data = fix_features_size(data, NUMBER_OF_FEATURES)
        # adding the 'point_of_view' field
        # data += root.split("/")[-1]
        a = str(np.random.randint(0, 3))
        print(a)
        data += str(a)
        all_data.append(data)
    return all_data

"""## Download our records dataset"""

# !rm -rf /content/*

# Delete the previeous data
# !rm -rf /content/*

# zipped_records_file_path = tf.keras.utils.get_file(fname=ZIPPED_DS_FILE_PATH, origin=zipped_records_url)

# print("Local copy of the records file: {}".format(zipped_records_file_path))

"""### Extracting

"""

# !unzip -n /content/DS.zip

"""## Creating the dataset from the AirSim records"""


def create_csv_dataset(files_names, number_of_features, dataset_filename):
    dataset = create_data_set(files_names)
    header_data = [len(dataset), number_of_features] + CLASS_NAMES
    dataset.insert(0, header_data)
    # Save the dataset as a CSV file in the wanted structure.
    save_list_to_CSV(dataset, dataset_filename)
    return dataset

# train_dataset_csv = create_csv_dataset(DS_FOLDER, TRAIN_FILE_EXTENTION, NUMBER_OF_FEATURES, TRAIN_DATASET_FILE_PATH)
#
# test_dataset_csv = create_csv_dataset(DS_FOLDER, TEST_FILE_EXTENTION, NUMBER_OF_FEATURES, TEST_DATASET_FILE_PATH)
#
# print(train_dataset_csv)
# print(test_dataset_csv)

##################################### works until here
def convert_array_dataset_to_Dense_dataset(_dataset):
    my_Dense_dataset = _dataset[1:]
    features = []
    labels = []
    for sample in my_Dense_dataset:
        tmp_features = sample[:-1]
        tmp_features = [float(i) for i in tmp_features]
        features += [tmp_features]
        labels += [int(float(sample[-1]))]  # we added the float () after the int
    labels = np.array(labels)
    features = np.array(features)
    return features, labels


# # np.reshape()
# Dense_features, Dense_labels = convert_array_dataset_to_Dense_dataset(train_dataset_csv)
# test_Dense_features, test_Dense_labels = convert_array_dataset_to_Dense_dataset(test_dataset_csv)
#
# print(test_Dense_features)
# print(test_Dense_labels)
# print(test_Dense_features.shape)


def convert_array_dataset_to_LSTM_dataset(_dataset):
    """
    split the _dataset to X = features and y= point_of_view (the predicted field)
    :param _dataset:
    :return: per flight, returns features (= list of flights (the GPS points))
    and labels (= list of start location for each flight in features)
    """
    my_LSTM_dataset = _dataset[1:]
    features = []
    labels = []
    for sample in my_LSTM_dataset:
        tmp_features = sample[:-1]
        tmp_features = [float(i) for i in tmp_features]
        features += [tmp_features]
        labels += [int(float(sample[-1]))]  # we added float() after the int
    labels = np.array(labels)
    features = np.array(features)
    features = features.reshape(len(_dataset) - 1, 1, NUMBER_OF_FEATURES) # the -1 is becose the headers line
    return features, labels

#
# # np.reshape()
# LSTM_features, LSTM_labels = convert_array_dataset_to_LSTM_dataset(train_dataset_csv)
# test_LSTM_features, test_LSTM_labels = convert_array_dataset_to_LSTM_dataset(test_dataset_csv)
#
# print(test_LSTM_features)
# print(test_LSTM_labels)
# print(LSTM_features.shape)
# print(LSTM_labels.shape)
# print(test_LSTM_features.shape)
#
# # !head -n10 {TRAIN_DATASET_FILE_PATH}
#
# # Looking our data is OK
# # !head -n7 {TRAIN_DATASET_FILE_PATH}
# print()
# # !head -n15 {TEST_DATASET_FILE_PATH}
#
"""##More functions"""

# all_labels = np.concatenate((LSTM_labels, test_LSTM_labels), axis=0)
# all_features = np.concatenate((LSTM_features, test_LSTM_features), axis=0)


def get_features_and_labels(features, labels, number_of_features):
    number_of_all_features, _, _ = features.shape
    number_of_labels = number_of_all_features - number_of_features
    labels_to_choose = np.zeros(number_of_all_features)

    training_features = np.zeros(NUMBER_OF_FEATURES).reshape(1, 1, 360)
    training_labels = np.array([])
    test_features = np.zeros(NUMBER_OF_FEATURES).reshape(1, 1, 360)
    test_labels = np.array([])

    for i in range(number_of_labels):
        random_cell = np.random.randint(0, number_of_all_features)
        while labels_to_choose[random_cell]:
            random_cell = np.random.randint(0, number_of_all_features)
        labels_to_choose[random_cell] = 1

    for i in range(number_of_all_features):
        if labels_to_choose[i] == 0:
            training_features = np.concatenate((training_features, [features[i]]))
            training_labels = np.concatenate((training_labels,[labels[i]]))
        else:
            test_features = np.concatenate((test_features, [features[i]]))
            test_labels = np.concatenate((test_labels, [labels[i]]))

    return training_features[1:], training_labels, test_features[1:], test_labels
#
#
# training_features, training_labels, test_features, test_labels = get_features_and_labels(415)
#
# # print(training_features.shape)
# # print(training_labels)
# # print(test_features.shape)
# # print(test_labels)
#
# _input_dim = 360  # 360
# #
# _units = 64
# # # _output_size = 3  # labels are from 0 to 9
# _output_size = 4  # labels are from 0 to 9
# #
# optimizer = 'sgd'
# metrics = ['accuracy']
#
#
def build_generic_model(first_layer, optimizer, metrics, output_size):
    model = tf.keras.models.Sequential([
        first_layer,
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(output_size)]
    )
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              optimizer=optimizer,
              metrics=metrics)
    return model
#
#
def build_GRU_model(input_dim, optimizer, metrics, output_size):
    RGU_layer = tf.keras.layers.GRU(_units, input_shape=(None, input_dim))
    model = tf.keras.models.Sequential([
        RGU_layer,
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(output_size)]
    )
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=optimizer,
                  metrics=metrics)
    return model


def build_LSTM_model(input_dim, optimizer, metrics, output_size):
    lstm_layer = tf.keras.layers.LSTM(_units, input_shape=(None, input_dim))
    model = tf.keras.models.Sequential([
        lstm_layer,
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(output_size)]
    )
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=optimizer,
                  metrics=metrics)
    return model


def build_DENSE_model(input_dim, optimizer, metrics, output_size):
    dense_layer = tf.keras.layers.Dense(_units, input_shape=(None, input_dim))
    model = tf.keras.models.Sequential([
        dense_layer,
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(output_size)]
    )
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=optimizer,
                  metrics=metrics)
    return model

# model_DENSE = build_DENSE_model()
# model_LSTM = build_LSTM_model()
# model_GRU = build_GRU_model()
#
# models = [("DENSE", model_DENSE), ("LSTM", model_LSTM), ("GRU", model_GRU)]
#
# for model_name, model in models:
#     model.summary()
#     tf.keras.utils.plot_model(model, to_file='model_' + model_name + '.png', show_shapes=True, show_layer_names=False)
#
# # Example
# model = build_DENSE_model()
#
# batch_size = 16
# # model.fit(x_train, y_train,
# model.fit(LSTM_features, LSTM_labels,
#           # validation_data=(x_test, y_test),
#           # validation_data=(test_LSTM_features, test_LSTM_labels),
#           batch_size=batch_size,
#           verbose=1,
#           epochs=8)  # 5
#
# model_evaluation = model.evaluate(test_LSTM_features, test_LSTM_labels, verbose=1)
# print(model_evaluation[1]*100)
#
#
def calc_model_average_succes(model_function, iterations, train_features, train_labels, test_features, test_labels, batch_size, epochs, model_name, verbose=0):
    eval_sum = 0
    for i in range(iterations):
        model = model_function()
        model.fit(train_features, train_labels,
              # validation_data=(test_LSTM_features, test_LSTM_labels),
              batch_size=batch_size,
              verbose=0,
              epochs=epochs)
        model_evaluation = model.evaluate(test_features, test_labels, verbose=verbose)
        eval_sum += model_evaluation[1]*100
        print(i, model_evaluation[1]*100)

    print()
    print(model_name + " sumerize: ")
    print(eval_sum/iterations)
#
#
# # def calc_generic_model_average_succes(first_layer, optimizer, metrics, iterations, batch_size, epochs, model_name, training_features=None, training_labels=None, test_features=None, test_labels=None, verbose=0):
def calc_generic_model_average_succes(input_dim, features, labels, optimizer, metrics,
                                      output_size, iterations, batch_size, epochs, model_name,
                                      neurons_in_layer, training_features=None, training_labels=None,
                                      test_features=None, test_labels=None, verbose=0):
    eval_sum = 0
    is_random_split = (training_features is None)
    results = []
    for i in range(iterations):
        first_layer = ""
        if model_name == "LSTM":
            first_layer = tf.keras.layers.LSTM(neurons_in_layer, input_shape=(None, input_dim))
        if model_name == "GRU":
            first_layer = tf.keras.layers.GRU(neurons_in_layer, input_shape=(None, input_dim))
        if model_name == "DENSE":
            first_layer = tf.keras.layers.Dense(neurons_in_layer, input_shape=(None, input_dim))
        if is_random_split:
            # split the dataset randomly to training and testing
            training_features, training_labels, test_features, test_labels = get_features_and_labels(features, labels, number_of_features=int(features.shape[0]*0.8))
        model = build_generic_model(first_layer, optimizer, metrics, output_size)
        model.fit(training_features, training_labels,
                  # validation_data=(test_LSTM_features, test_LSTM_labels),
                  batch_size=batch_size,
                  verbose=0,
                  epochs=epochs)
        model_evaluation = model.evaluate(test_features, test_labels, verbose=verbose)
        eval_sum += model_evaluation[1]*100
        results.append(model_evaluation[1]*100)

    results_np = np.array(results)
    sumery_str = ""
    sumery_str += ("mean = " + "%.5f" % results_np.mean())
    sumery_str += (", std: " + "%.5f" % results_np.std())
    sumery_str += (", model_name:" + model_name)
    sumery_str += (", optimizer:" + optimizer)
    sumery_str += (", iterations:" + str(iterations))
    sumery_str += (", batch_size:" + str(batch_size))
    sumery_str += (", epochs:" + str(epochs))
    sumery_str += (", neurons_in_layer:" + str(neurons_in_layer))
    sumery_str += (", min: " + "%.5f" % results_np.min())
    sumery_str += (", max: " + "%.5f" % results_np.max())
    sumery_str += (", results: " + str(list(map(lambda x: "%.5f" % x, results))))
    print(sumery_str)

#
# """##Creating and testing models"""
#
# # Part of tests
#
# # models_names = ["DENSE", "GRU", "LSTM"]
# models_names = ["LSTM"]
# # _units = 64
# # neurons_in_layer_arr = [64, 124]
# neurons_in_layer_arr = [124]
#
# # optimizers = ['sgd', 'adam'];
# optimizers = ['adam']
# batch_sizes = [24, 30]
# epochss = [3, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 33, 36]
#
# metrics = ['accuracy']
#
# iterations = 50
#
# for model_name in models_names:
#     for neurons_in_layer in neurons_in_layer_arr:
#         for optimizer in optimizers:
#             for batch_size in batch_sizes:
#                 for epochs in epochss:
#                     calc_generic_model_average_succes(optimizer, metrics, iterations,
#                                                       batch_size, epochs, model_name, neurons_in_layer, verbose=0)
#     print()
#
# print("DONE!!!!!")
#
# # NEW BIGGEST!!!!!!!
# # part 6.2
# # ADAM
# # 124 neurons, LSTM
#
# # models_names = ["DENSE", "GRU", "LSTM"]
# # models_names = ["GRU", "LSTM"]
# models_names = ["LSTM"]
# # _units = 64
# # neurons_in_layer_arr = [64, 124]
# neurons_in_layer_arr = [124]
#
# # optimizers = ['sgd', 'adam'];
# optimizers = ['adam']
# batch_sizes = [2, 4, 6, 10, 16, 24, 30]
# epochss = [3, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 33, 36]
#
# metrics = ['accuracy']
#
# iterations = 50
#
# for model_name in models_names:
#     for neurons_in_layer in neurons_in_layer_arr:
#         for optimizer in optimizers:
#             for batch_size in batch_sizes:
#                 for epochs in epochss:
#                     calc_generic_model_average_succes(optimizer, metrics, iterations, batch_size, epochs, model_name, neurons_in_layer, verbose=0)
#     print()
#
# print("DONE!!!!!")
#
# # NEW best results! (tring for 300 iterations)
# # part find best params
# # ALL
#
# models_names = ["DENSE", "GRU", "LSTM"]
# neurons_in_layer_arr = [64, 124]
# optimizers = ['sgd', 'adam']
# batch_sizes = [2, 4, 6, 10, 16, 24, 30]
# epochss = [3, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 33, 36]
# metrics = ['accuracy']
#
# # model_name, optimizer, batch_size, epochs, neurons_in_layer
# top_results = [
#           ("DENSE",	"sgd",	10,	28,	64),
#           ("DENSE",	"adam",	24,	36,	64),
#           ("DENSE",	"adam",	16,	30,	64),
#           ("DENSE",	"adam",	10,	33,	64),
#           ("DENSE",	"adam",	10,	30,	64),
#           ("DENSE",	"sgd",	10,	26,	64),
#
#           ("GRU",		"adam",	6,	36,	64),
#           ("GRU",		"adam",	6,	30,	64),
#           ("GRU",		"adam",	6,	28,	64),
#           ("GRU",		"adam",	4,	33,	64),
#           ("GRU",		"adam",	4,	22,	64),
#           ("GRU",		"adam",	4,	30,	124),
#
#           ("LSTM",	"adam",	10,	30,	64),
#           ("LSTM",	"adam",	4,	36,	64),
#           ("LSTM",	"adam",	6,	36,	64),
#           ("LSTM",	"adam",	10,	33,	64),
#           ("LSTM",	"adam",	6,	28,	64),
#           ("LSTM",	"adam",	16,	33,	64)
# ]
#
# iterations = 300
#
# for model_name, optimizer, batch_size, epochs, neurons_in_layer in top_results:
#     calc_generic_model_average_succes(optimizer, metrics, iterations, batch_size,
#                                       epochs, model_name, neurons_in_layer, verbose=0)
#
# # for model_name in models_names:
# #   for neurons_in_layer in neurons_in_layer_arr:
# #     for optimizer in optimizers:
# #       for batch_size in batch_sizes:
# #         for epochs in epochss:
# #           calc_generic_model_average_succes(optimizer, metrics, iterations, batch_size, epochs, model_name, neurons_in_layer, verbose=0)
#   # print()
#
# print("DONE!!!!!")


if __name__ == '__main__':
    # 1. split data to 80% train and 20% test (creates 2 folders - Train and Test)
    train_files = []
    test_files = []
    for root, __, files in os.walk(DS_FOLDER):
        train_files, test_files = train_test_split(files, test_size=.20, shuffle=True)

    # 2. create data sets for train and test
    train_dataset_csv = create_csv_dataset(train_files, NUMBER_OF_FEATURES, TRAIN_DATASET_FILE_PATH)
    test_dataset_csv = create_csv_dataset(test_files, NUMBER_OF_FEATURES, TEST_DATASET_FILE_PATH)
    print(train_dataset_csv)
    print(test_dataset_csv)

    # 3. data preparation: test_Dense_features= [[GPS points flight 1],[GPS points flight 2],,,]
    Dense_features, Dense_labels = convert_array_dataset_to_Dense_dataset(train_dataset_csv)
    test_Dense_features, test_Dense_labels = convert_array_dataset_to_Dense_dataset(test_dataset_csv)

    # print(test_Dense_features)
    # print(test_Dense_labels)
    # print(test_Dense_features.shape)

    # convert array dataset to LSTM dataset. LSTM_features = x_train, LSTM_labels = y_train
    # test_LSTM_features = x_test, test_LSTM_labels = y_test
    LSTM_features, LSTM_labels = convert_array_dataset_to_LSTM_dataset(train_dataset_csv)
    test_LSTM_features, test_LSTM_labels = convert_array_dataset_to_LSTM_dataset(test_dataset_csv)

    print(test_LSTM_features)
    print(test_LSTM_labels)
    print(LSTM_features.shape)
    print(LSTM_labels.shape)
    print(test_LSTM_features.shape)

    # concat labels and features of the train set and the test set
    all_labels = np.concatenate((LSTM_labels, test_LSTM_labels), axis=0)
    all_features = np.concatenate((LSTM_features, test_LSTM_features), axis=0)
    print(all_features.shape)
    num_of_features, _, _ = all_features.shape
    # final X_train, y_train, X_test and y_test
    training_features, training_labels, test_features, test_labels = get_features_and_labels(all_features, all_labels, int(num_of_features*0.8))

    print(training_features.shape)
    print(training_labels)
    print(test_features.shape)
    print(test_labels)

    # 4. create model parameters
    _input_dim = 360  # 360 is the number of features, size of input. 3*120 [3 is xyz, 120 is samples during the flight].
    # 3 layers in each model, last one is dense
    _units = 64  # num of neurons, going to change
    _output_size = 4  # labels are from 0 to 9

    optimizer = 'sgd'
    metrics = ['accuracy']

    # 5. create 3 types of models
    model_DENSE = build_DENSE_model(_input_dim, optimizer, metrics, _output_size)
    model_LSTM = build_LSTM_model(_input_dim, optimizer, metrics, _output_size)
    model_GRU = build_GRU_model(_input_dim, optimizer, metrics, _output_size)

    models = [("DENSE", model_DENSE), ("LSTM", model_LSTM), ("GRU", model_GRU)]
    # find the plots on the left, in the folder
    for model_name, model in models:
        model.summary()
        # tf.keras.utils.plot_model(model, to_file='model_' + model_name + '.png', show_shapes=True, show_layer_names=False)

    # # Example 1 --------------------------------
    # model = build_DENSE_model(_input_dim, optimizer, metrics, _output_size)
    #
    # batch_size = 16
    # # model.fit(x_train, y_train,
    # model.fit(LSTM_features, LSTM_labels,
    #           # validation_data=(x_test, y_test),
    #           # validation_data=(test_LSTM_features, test_LSTM_labels),
    #           batch_size=batch_size,
    #           verbose=1,
    #           epochs=8)  # 5
    #
    # model_evaluation = model.evaluate(test_LSTM_features, test_LSTM_labels, verbose=1)
    # print(model_evaluation[1]*100)
    # # end Example 1 --------------------------------

    """##Creating and testing models"""
    # # Example 2 - ------------------------------------
    # Part of tests
    models_names = ["LSTM"]
    neurons_in_layer_arr = [124]

    optimizers = ['adam']
    # batch_sizes = [24, 30]
    batch_sizes = [24]
    # epochss = [3, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 33, 36]
    epochss = [3]
    metrics = ['accuracy']
    iterations = 50

    # this for loop can be maybe in the reports
    for model_name in models_names:
        for neurons_in_layer in neurons_in_layer_arr:
            for optimizer in optimizers:
                for batch_size in batch_sizes:
                    for epochs in epochss:
                        calc_generic_model_average_succes(_input_dim, all_features, all_labels, optimizer, metrics, _output_size, iterations,
                                                          batch_size, epochs, model_name, neurons_in_layer, verbose=0)
        print()

    print("DONE!!!!!")
    # # End Example 2 - ------------------------------------

    # # NEW BIGGEST!!!!!!!
    # # part 6.2
    # # ADAM
    # # 124 neurons, LSTM
    #
    # # models_names = ["DENSE", "GRU", "LSTM"]
    # # models_names = ["GRU", "LSTM"]
    # models_names = ["LSTM"]
    # # _units = 64
    # # neurons_in_layer_arr = [64, 124]
    # neurons_in_layer_arr = [124]
    #
    # # optimizers = ['sgd', 'adam'];
    # optimizers = ['adam']
    # batch_sizes = [2, 4, 6, 10, 16, 24, 30]
    # epochss = [3, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 33, 36]
    #
    # metrics = ['accuracy']
    #
    # iterations = 50
    #
    # for model_name in models_names:
    #     for neurons_in_layer in neurons_in_layer_arr:
    #         for optimizer in optimizers:
    #             for batch_size in batch_sizes:
    #                 for epochs in epochss:
    #                     calc_generic_model_average_succes(optimizer, metrics, iterations, batch_size, epochs, model_name, neurons_in_layer, verbose=0)
    #     print()
    #
    # print("DONE!!!!!")
    #
    # # NEW best results! (tring for 300 iterations)
    # # part find best params
    # # ALL
    #
    # models_names = ["DENSE", "GRU", "LSTM"]
    # neurons_in_layer_arr = [64, 124]
    # optimizers = ['sgd', 'adam']
    # batch_sizes = [2, 4, 6, 10, 16, 24, 30]
    # epochss = [3, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 33, 36]
    # metrics = ['accuracy']
    #
    # # model_name, optimizer, batch_size, epochs, neurons_in_layer
    # top_results = [
    #           ("DENSE",	"sgd",	10,	28,	64),
    #           ("DENSE",	"adam",	24,	36,	64),
    #           ("DENSE",	"adam",	16,	30,	64),
    #           ("DENSE",	"adam",	10,	33,	64),
    #           ("DENSE",	"adam",	10,	30,	64),
    #           ("DENSE",	"sgd",	10,	26,	64),
    #
    #           ("GRU",		"adam",	6,	36,	64),
    #           ("GRU",		"adam",	6,	30,	64),
    #           ("GRU",		"adam",	6,	28,	64),
    #           ("GRU",		"adam",	4,	33,	64),
    #           ("GRU",		"adam",	4,	22,	64),
    #           ("GRU",		"adam",	4,	30,	124),
    #
    #           ("LSTM",	"adam",	10,	30,	64),
    #           ("LSTM",	"adam",	4,	36,	64),
    #           ("LSTM",	"adam",	6,	36,	64),
    #           ("LSTM",	"adam",	10,	33,	64),
    #           ("LSTM",	"adam",	6,	28,	64),
    #           ("LSTM",	"adam",	16,	33,	64)
    # ]
    #
    # iterations = 300
    #
    # for model_name, optimizer, batch_size, epochs, neurons_in_layer in top_results:
    #     calc_generic_model_average_succes(optimizer, metrics, iterations, batch_size,
    #                                       epochs, model_name, neurons_in_layer, verbose=0)
    #
    # # for model_name in models_names:
    # #   for neurons_in_layer in neurons_in_layer_arr:
    # #     for optimizer in optimizers:
    # #       for batch_size in batch_sizes:
    # #         for epochs in epochss:
    # #           calc_generic_model_average_succes(optimizer, metrics, iterations, batch_size, epochs, model_name, neurons_in_layer, verbose=0)
    #   # print()
    #
    # print("DONE!!!!!")