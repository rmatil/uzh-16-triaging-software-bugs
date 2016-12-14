import os.path as path
import csv

from matplotlib import pyplot as plt
from sklearn.metrics import roc_curve

from model import LinearModel
from model import NeuralNet
from model import TreeModel
from setup import Sampler

# Predict results using different models

database = "../resources/database/bug_reports.db"
database = path.abspath(database)

sampler = Sampler.DbSampler(database, 'training_set', 'validation_set', 'test_set')

# obtain training and test data
X_train, y_train = sampler.getTrainingData()
X_validation, y_validation = sampler.getValidationData()
X_test, y_test = sampler.getTestData()

cross_validation_k = 5

print('Using classic linear regression to evaluate...')
regression = LinearModel.LinRegression(X_train, y_train, X_test, y_test, cross_validation_k)
accuracy, f1_score, lin_reg_y_prediction, lin_reg_cv_score = regression.evaluate()
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using lasso linear regression to evaluate...')
lasso_reg = LinearModel.LassoRegression(X_train, y_train, X_test, y_test, cross_validation_k)
accuracy, f1_score, lasso_reg_y_prediction, lasso_reg_cv_score = lasso_reg.evaluate(alpha=0.5)
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using logistic regression to evaluate...')
log_reg = LinearModel.LogisticRegression(X_train, y_train, X_test, y_test, cross_validation_k)
accuracy, f1_score, log_reg_y_prediction, log_reg_cv_score = log_reg.evaluate(penalty='l1')
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using bayesian ridge regression to evaluate...')
bay_reg = LinearModel.BayesianRegression(X_train, y_train, X_test, y_test, cross_validation_k)
accuracy, f1_score, bay_reg_y_prediction, bay_reg_cv_score = bay_reg.evaluate(penalty='l1')
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using decision tree to evaluate...')
tree = TreeModel.DecisionTree(X_train, y_train, X_test, y_test, cross_validation_k)
accuracy, f1_score, dec_tree_y_prediction, dec_tree_cv_score = tree.evaluate(create_image=False)
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using neural net to evaluate...')
nn = NeuralNet.DeepModel(X_train, y_train, X_validation, y_validation, X_test, y_test)
accuracy, f1_score, nn_y_predictions = nn.evaluate()
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

print('Using optimized neural net to evaluate...')
opt_nn = NeuralNet.OptimizedDeepModel(db_name=database)
accuracy, f1_score, optimized_nn_y_predictions = opt_nn.evaluate()
print('Achieved accuracy of %s and f1 score of %s' % (accuracy, f1_score))

linewidth = 1
# Create ROC figure
plt.figure(1, dpi=3600, figsize=(8, 5))

fpr, tpr, thresholds = roc_curve(y_test, lin_reg_y_prediction)
plt.plot(fpr, tpr, lw=linewidth, label='linear regression')

fpr, tpr, thresholds = roc_curve(y_test, lasso_reg_y_prediction)
plt.plot(fpr, tpr, lw=linewidth, label='lasso regression')

fpr, tpr, thresholds = roc_curve(y_test, log_reg_y_prediction)
plt.plot(fpr, tpr, lw=linewidth, label='logistic regression')

fpr, tpr, thresholds = roc_curve(y_test, bay_reg_y_prediction)
plt.plot(fpr, tpr, lw=linewidth, label='bayesian ridge regression')

fpr, tpr, thresholds = roc_curve(y_test, dec_tree_y_prediction)
plt.plot(fpr, tpr, lw=linewidth, label='decision tree')

fpr, tpr, thresholds = roc_curve(y_test, nn_y_predictions)
plt.plot(fpr, tpr, lw=linewidth, label='neural net')

opt_nn_X_test, opt_nn_y_test = opt_nn.getTestData()
fpr, tpr, thresholds = roc_curve(opt_nn_y_test, optimized_nn_y_predictions)
plt.plot(fpr, tpr, lw=linewidth, label='optimized neural net')

plt.plot([0, 1], [0, 1], color='navy', lw=linewidth, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('../resources/output/roc_curves.png')


# Figure for Cross Validation metrics
plt.figure(2, dpi=3600, figsize=(8, 5))

plt.plot(lin_reg_cv_score, lw=linewidth, label='linear regression')
plt.plot(lasso_reg_cv_score, lw=linewidth, label='lasso regression')
plt.plot(log_reg_cv_score, lw=linewidth, label='logistic regression')
plt.plot(bay_reg_cv_score, lw=linewidth, label='bayesian ridge regression')
plt.plot(dec_tree_cv_score, lw=linewidth, label='decision tree')

plt.xlim([0, cross_validation_k + 1])
plt.ylim([0, 1.05])
plt.xlabel('k')
plt.ylabel('Score')
plt.title('K-Fold Cross Validation Score for k=%s' % cross_validation_k)
plt.legend(loc="lower right")
plt.savefig('../resources/output/cross_validation_scores.png')

# since the decision tree model was the best one
# use it as final predictor for submission

bug_ids = sampler.getTestBugIds()


bug_ids = list([x[0] for x in bug_ids])
predictions = list([1 if x > 0.5 else 0 for x in dec_tree_y_prediction])

rows = []
for x in range(0, len(bug_ids)):
    rows.append((bug_ids[x], predictions[x]))

with open('../resources/output/predictions.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(rows)
