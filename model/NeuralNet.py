import sqlite3

import numpy as np
from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.optimizers import SGD
from sklearn.metrics import f1_score, accuracy_score


class NNModel(object):
    """
        Base class for neural net models

        Initializes the neural net model with data. Note, that the training data samples and labels
        have to be of the same length. Same also for test data

        :param X_train: A matrix of the form [n samples, n features]
        :param y_train: A vector containing the labels for the training data
        :param X_validation: A matrix of the form [n samples, n features]
        :param y_validation: A vector containing the labels for the validation data
        :param X_test: A matrix of the form [n samples, n features]
        :param y_test: A vector containing the labels for the test data
    """

    def __init__(self, X_train, y_train, X_validation, y_validation, X_test, y_test):
        self._X_train = X_train
        self._y_train = y_train
        self._X_validation = X_validation
        self._y_validation = y_validation
        self._X_test = X_test
        self._y_test = y_test

    def evaluate(self):
        """
        Evaluates the model

        :return: As first param the accuracy, as second param the f1 score and as third the actual predicted values
        """
        raise NotImplementedError('Implement in subclass')


class DeepModel(NNModel):
    """
        Uses a neural net with two layers in order to predict values

        Initializes the neural net model with data. Note, that the training data samples and labels
        have to be of the same length. Same also for test data

        :param X_train: A matrix of the form [n samples, n features]
        :param y_train: A vector containing the labels for the training data
        :param X_validation: A matrix of the form [n samples, n features]
        :param y_validation: A vector containing the labels for the validation data
        :param X_test: A matrix of the form [n samples, n features]
        :param y_test: A vector containing the labels for the test data
    """

    def __init__(self, X_train, y_train, X_validation, y_validation, X_test, y_test):
        super().__init__(X_train, y_train, X_validation, y_validation, X_test, y_test)

        # do not use all features
        # self._X_train = self._X_train[:, [0, 1, 2, 3]]
        # self._X_validation = self._X_validation[:, [0, 1, 2, 3]]
        # self._X_test = self._X_test[:, [0, 1, 2, 3]]
        #
        # print(self._X_train[0])
        # print(len(self._X_train), len(self._X_validation), len(self._X_test))

    def evaluate(self):
        model = Sequential()
        model.add(Dense(9, input_dim=self._X_train.shape[1]))
        model.add(Activation('linear'))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))

        model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.01), metrics=['accuracy'])

        model.fit(self._X_train, self._y_train, batch_size=50, nb_epoch=5,
                  validation_data=(self._X_validation, self._y_validation))
        y_predictions = model.predict(self._X_test, batch_size=50)

        # assume that everything which was predicted with p > 0.5 is positive
        predictions = [1 if x > 0.5 else 0 for x in y_predictions]

        return accuracy_score(self._y_test, predictions), f1_score(self._y_test, predictions), y_predictions


class OptimizedDeepModel(object):
    """
        This is an optimized version of the same neural net as DeepModel,
        but it uses different data in order to train and evaluate.
    """

    def __init__(self, db_name):
        """
            :param db_name: The name and path to the database storing the features
        """
        self._connection = sqlite3.connect(db_name)
        self._init()

    def _init(self):
        """
            Retrieves the first 120000 entries from the dataset as training data and again 30000 as test data
        """
        cursor = self._connection.cursor()

        cursor.execute(
            'SELECT feature_1, feature_2, feature_3, feature_4, success FROM (SELECT reports.bug_id, feature_1, feature_2, feature_3, feature_4, 1 AS success FROM (SELECT * FROM reports INNER JOIN features ON features.bug_id = reports.bug_id LIMIT 0, 120000) AS reports WHERE feature_1 NOT NULL AND feature_2 NOT NULL AND feature_3 NOT NULL AND feature_4 NOT NULL AND ( current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR current_status == "CLOSED" AND reports.current_resolution == "FIXED") UNION SELECT reports.bug_id, feature_1, feature_2, feature_3, feature_4, 0 AS success FROM (SELECT * FROM reports INNER JOIN features ON features.bug_id = reports.bug_id LIMIT 0, 120000) AS reports WHERE feature_1 NOT NULL AND feature_2 NOT NULL AND feature_3 NOT NULL AND feature_4 NOT NULL AND ( reports.current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR reports.current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR reports.current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR reports.current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR reports.current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR reports.current_status == "VERIFIED" AND reports.current_resolution == "INVALID") )')
        X_train_y_train = cursor.fetchall()
        X_train_y_train = np.array(X_train_y_train)

        # split this shit up into training data and corresponding labels
        X_train = X_train_y_train[:, [0, 1, 2, 3]]
        y_train = X_train_y_train[:, [4]]

        cursor.execute(
            'SELECT feature_1, feature_2, feature_3, feature_4, success FROM (SELECT reports.bug_id, feature_1, feature_2, feature_3, feature_4, 1 AS success FROM (SELECT * FROM reports INNER JOIN features ON features.bug_id = reports.bug_id LIMIT 120001, 150000) AS reports WHERE feature_1 NOT NULL AND feature_2 NOT NULL AND feature_3 NOT NULL AND feature_4 NOT NULL AND ( current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR current_status == "CLOSED" AND reports.current_resolution == "FIXED") UNION SELECT reports.bug_id, feature_1, feature_2, feature_3, feature_4, 0 AS success FROM (SELECT * FROM reports INNER JOIN features ON features.bug_id = reports.bug_id LIMIT 120001, 150000) AS reports WHERE feature_1 NOT NULL AND feature_2 NOT NULL AND feature_3 NOT NULL AND feature_4 NOT NULL AND ( reports.current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR reports.current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR reports.current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR reports.current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR reports.current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR reports.current_status == "VERIFIED" AND reports.current_resolution == "INVALID") )')
        X_test_y_test = cursor.fetchall()
        X_test_y_test = np.array(X_test_y_test)

        # split this shit up into training data and corresponding labels
        X_test = X_test_y_test[:, [0, 1, 2, 3]]
        y_test = X_test_y_test[:, [4]]

        if X_train.shape[0] != y_train.shape[0] or X_test.shape[0] != y_test.shape[0]:
            raise Exception("There are not an equal size of labels and samples")

        self._X_train = X_train
        self._y_train = y_train
        self._X_test = X_test
        self._y_test = y_test

    def getTrainingData(self):
        """
        Returns the used training data an its labels

        :return: np.array, np.array
        """
        return self._X_train, self._y_train

    def getTestData(self):
        """
            Returns the used test data an its labels

            :return: np.array, np.array
        """
        return self._X_test, self._y_test

    def evaluate(self):
        """
            Evaluates the model based on the fetched training and test data

            :return: As 1st parameter the accuracy, as 2nd the f1 score and as 3rd the achieved predictions on the test set
        """
        model = Sequential()
        model.add(Dense(5, input_dim=self._X_train.shape[1]))
        model.add(Activation('sigmoid'))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

        model.fit(self._X_train, self._y_train, batch_size=50, nb_epoch=5)
        y_predictions = model.predict(self._X_test, batch_size=50)

        # assume that everything which was predicted with p > 0.5 is positive
        predictions = [1 if x > 0.5 else 0 for x in y_predictions]

        return accuracy_score(self._y_test, predictions), f1_score(self._y_test, predictions), y_predictions
