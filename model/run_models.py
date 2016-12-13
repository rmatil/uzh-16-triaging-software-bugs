import os.path as path

from setup import Sampler
from model import LinearModel
from model import NeuralNet

database = "../resources/database/bug_reports.db"
database = path.abspath(database)

sampler = Sampler.DbSampler(database, 'training_set', 'validation_set', 'test_set')

# obtain training and test data
X_train, y_train = sampler.getTrainingData()
X_validation, y_validation = sampler.getValidationData()
X_test, y_test = sampler.getTestData()

print('Using classic linear regression to evaluate...')
regression = LinearModel.LinRegression(X_train, y_train, X_test, y_test)
accuracy, f1_score = regression.evaluate()
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using lasso linear regression to evaluate...')
regression = LinearModel.LassoRegression(X_train, y_train, X_test, y_test)
accuracy, f1_score = regression.evaluate(alpha=0.5)
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using logistic regression to evaluate...')
regression = LinearModel.LogisticRegression(X_train, y_train, X_test, y_test)
accuracy, f1_score = regression.evaluate(penalty='l1')
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using neural net to evaluate...')
nn = NeuralNet.DeepModel(X_train, y_train, X_validation, y_validation, X_test, y_test)
accuracy, f1_score = nn.evaluate()
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))
