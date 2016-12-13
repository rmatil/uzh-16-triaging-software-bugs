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

        model.fit(self._X_train, self._y_train, batch_size=50, nb_epoch=5, validation_data=(self._X_validation, self._y_validation))
        y_predictions = model.predict(self._X_test, batch_size=50)

        # assume that everything which was predicted with p > 0.5 is positive
        predictions = [1 if x > 0.5 else 0 for x in y_predictions]

        return accuracy_score(self._y_test, predictions), f1_score(self._y_test, predictions), y_predictions
