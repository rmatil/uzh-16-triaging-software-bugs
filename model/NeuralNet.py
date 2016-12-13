from keras.layers import Dense, Activation
from keras.models import Sequential


class NNModel(object):
    """Base class for neural net models"""

    def __init__(self, X_train, y_train, X_validation, y_validation, X_test, y_test):
        """
        Initializes the neural net model with data. Note, that the training data samples and labels
        have to be of the same length. Same also for test data

        :param X_train: A matrix of the form [n samples, n features]
        :param y_train: A vector containing the labels for the training data
        :param X_test: A matrix of the form [n samples, n features]
        :param y_test: A vector containing the labels for the test data
        """
        self._X_train = X_train
        self._y_train = y_train
        self._X_validation = X_validation
        self._y_validation = y_validation
        self._X_test = X_test
        self._y_test = y_test

    def evaluate(self):
        """
        Evaluates the model

        :return: As first param the accuracy and as second param the f1 score
        """
        raise NotImplementedError('Implement in subclass')


class DeepModel(NNModel):
    def __init__(self, X_train, y_train, X_validation, y_validation, X_test, y_test):
        super().__init__(X_train, y_train, X_validation, y_validation, X_test, y_test)

    def evaluate(self):
        model = Sequential()
        model.add(Dense(5, input_dim=self._X_train.shape[1]))
        model.add(Activation('sigmoid'))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

        model.fit(self._X_train, self._y_train, batch_size=50, nb_epoch=9, validation_data=(self._X_validation, self._y_validation))
        score, acc = model.evaluate(self._X_test, self._y_test, batch_size=50)

        # print an empty line
        print()

        return acc, score
