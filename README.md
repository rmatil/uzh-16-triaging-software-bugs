# uzh-16-triaging-software-bugs
The final project in the course Business Analytics at UZH: Classifying whether a bug should be fixed based on the [MSR 2013 dataset](https://github.com/ansymo/msr2013-bug_dataset)

## Installation
*Note*, that for cloning this repo, Git LFS is recommended in order to download the previously created database

#### Requirements
* Python >= 3.5
* Numpy
* Pydotplus
* Keras: [keras.io](http://keras.io)
* Theano: [http://www.deeplearning.net/software/theano/](http://www.deeplearning.net/software/theano/) (If you want to try the neural network approach)

## Setup
The project is already set up in so that you can run the different approaches out of the box. 
In case you want to update some features, note the following
* Run [`setup.py`](https://github.com/rmatil/uzh-16-triaging-software-bugs/blob/master/setup/setup.py) in the `setup` directory in order to create a database storing the features as well as the bug data
* Run [`extract_features.py`](https://github.com/rmatil/uzh-16-triaging-software-bugs/blob/master/setup/extract_features.py) in the `setup` directory in order to extract the features from the bug data. *NOTE*, that this will consume a lot of time (expect some hours)
* Run [`sample.py`](https://github.com/rmatil/uzh-16-triaging-software-bugs/blob/master/setup/sample.py) in the `setup` directory in order to create shuffled data for training, validation and testing

## Features
*Note:* These features are also explained in further detail in [RPICase.pdf](https://github.com/rmatil/uzh-16-triaging-software-bugs/blob/master/RPICase.pdf)
* Feature 1: Success Rate of a bug assignee
* Feature 2: Success Rate of a bug reporter
* Feature 3: Success Ratio of a bug report for every reporter-assignee pair
* Feature 4: Success Ratio of a bug in terms of how many times it got reassigned
* Feature 5: Number of reassignments of a bug
* Feature 6: The duration in seconds of how long a bug was opened
* Feature 7: Success Ratio of the component to which the bug was assigned
* Feature 8: Success Ratio of a bug considering the reporter and all names on the CC 
* Feature 9: Success Ratio of the version to which the bug was assigned
* Feature 10: Success Ratio of a bug depending whether it is classified as user interface, environment or network related

## Models
In order to apply the models to the different features, run [`run_models.py`](https://github.com/rmatil/uzh-16-triaging-software-bugs/blob/master/model/run_models.py) within the `model` directory.
You get as output the accuracy as well as the f1 score for each model on the test data.

Interpreting the prediction results: `1` represents, that a bug was fixed, `0` that it will not be fixed

## Results
The following image represents a ROC curve over the used models

![ROC curves for different models](/resources/output/roc_curves.png?raw=true)
