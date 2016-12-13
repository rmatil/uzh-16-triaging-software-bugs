import os.path as path

import numpy as np
import pydotplus
from sklearn import tree
from sklearn.metrics import f1_score, accuracy_score


class TreeModel(object):
    """
        Base class for decision trees

        Initializes the linear model with data. Note, that the training data samples and labels
        have to be of the same length. Same also for test data

        :param X_train: A matrix of the form [n samples, n features]
        :param y_train: A vector containing the labels for the training data
        :param X_test: A matrix of the form [n samples, n features]
        :param y_test: A vector containing the labels for the test data
    """

    def __init__(self, X_train, y_train, X_test, y_test):
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


class DecisionTree(TreeModel):
    """
        Decision tree

        Initializes the linear model with data. Note, that the training data samples and labels
        have to be of the same length. Same also for test data

        :param X_train: A matrix of the form [n samples, n features]
        :param y_train: A vector containing the labels for the training data
        :param X_test: A matrix of the form [n samples, n features]
        :param y_test: A vector containing the labels for the test data
    """
    def __init__(self, X_train, y_train, X_test, y_test):
        super().__init__(X_train, y_train, X_test, y_test)

    def evaluate(self, **kwargs):
        """
            Pass 'create_image=True' to create an image of the decision tree
        """
        create_image = kwargs.get('create_image', False)

        # Flatten matrix of size (n samples, 1) to an array of size (n samples,)
        self._y_train = np.ravel(self._y_train)
        self._y_test = np.ravel(self._y_test)

        decision_tree = tree.DecisionTreeClassifier()
        decision_tree.fit(self._X_train, self._y_train)

        # Create a pdf of the decision tree
        if create_image:
            outpath = "../resources/output/decision_tree.pdf"
            print('[DecisionTree] Creating image of decision tree at %s' % path.abspath(outpath))

            dot_data = tree.export_graphviz(decision_tree, out_file=None)
            graph = pydotplus.graph_from_dot_data(dot_data)
            graph.write_pdf(outpath)

            print('[DecisionTree] Done')

        predictions = decision_tree.predict(self._X_test)

        # assume that everything which was predicted with p > 0.5 is positive
        predictions = [1 if x > 0.5 else 0 for x in predictions]

        return accuracy_score(self._y_test, predictions), f1_score(self._y_test, predictions)
