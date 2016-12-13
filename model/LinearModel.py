from sklearn import linear_model
from sklearn.metrics import f1_score, accuracy_score

import numpy as np


class LinModel(object):
    """Base class for linear models"""

    def __init__(self, X_train, y_train, X_test, y_test):
        """
        Initializes the linear model with data. Note, that the training data samples and labels
        have to be of the same length. Same also for test data

        :param X_train: A matrix of the form [n samples, n features]
        :param y_train: A vector containing the labels for the training data
        :param X_test: A matrix of the form [n samples, n features]
        :param y_test: A vector containing the labels for the test data
        """
        self._X_train = X_train
        self._y_train = y_train
        self._X_test = X_test
        self._y_test = y_test

    def evaluate(self):
        """
        Evaluates the model

        :return: As first param the accuracy and as second param the f1 score
        """
        raise NotImplementedError('Implement in subclass')


class LinRegression(LinModel):
    """Linear regression"""

    def __init__(self, X_train, y_train, X_test, y_test):
        super().__init__(X_train, y_train, X_test, y_test)

    def evaluate(self, **kwargs):
        reg = linear_model.LinearRegression()
        reg.fit(self._X_train, self._y_train)

        predictions = reg.predict(self._X_test)

        # assume that everything which was predicted with p > 0.5 is positive
        predictions = [1 if x > 0.5 else 0 for x in predictions]

        return accuracy_score(self._y_test, predictions), f1_score(self._y_test, predictions)


class LassoRegression(LinModel):
    """Lasso regression"""

    def __init__(self, X_train, y_train, X_test, y_test):
        super().__init__(X_train, y_train, X_test, y_test)

    def evaluate(self, **kwargs):
        alpha = kwargs.get('alpha', 1.0)

        reg = linear_model.Lasso(alpha=alpha)
        reg.fit(self._X_train, self._y_train)

        predictions = reg.predict(self._X_test)

        # assume that everything which was predicted with p > 0.5 is positive
        predictions = [1 if x > 0.5 else 0 for x in predictions]

        return accuracy_score(self._y_test, predictions), f1_score(self._y_test, predictions)


class LogisticRegression(LinModel):
    """Logistic regression"""

    def __init__(self, X_train, y_train, X_test, y_test):
        super().__init__(X_train, y_train, X_test, y_test)

    def evaluate(self, **kwargs):
        penalty = kwargs.get('penalty', 'l2')

        # Flatten matrix of size (n samples, 1) to an array of size (n samples,)
        self._y_train = np.ravel(self._y_train)
        self._y_test = np.ravel(self._y_test)

        reg = linear_model.LogisticRegression(penalty=penalty)
        reg.fit(self._X_train, self._y_train)

        predictions = reg.predict(self._X_test)

        # assume that everything which was predicted with p > 0.5 is positive
        predictions = [1 if x > 0.5 else 0 for x in predictions]

        return accuracy_score(self._y_test, predictions), f1_score(self._y_test, predictions)
