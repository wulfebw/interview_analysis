""" 
filename: predict.py
date: 3/13/15
description: This file contains methods for predicting target values with a specific model and given sample features.

todo:
	(1) figure out how to load a model (using some generic value passed in that can grab the correct model)
	(2) be passed a set of features (in the correct order?) 
	(3) make a prediction using the loaded model
	(4) return the prediction

[Q]
	how to ensure ordering of features
	how to ensure the features used throughout remain constant?

"""

from sklearn import svm

def load_model(feature_name):
	"""
	Loads a pretrained model and returns it.

	[Q] 
		what does this return?
		options:
				(1) a sklearn classifier
					- doesn't matter which type of model since you can just call predict()
	"""
	filename = feature_name + '.p'
	path = '/Users/wulfe/Dropbox/Start/flask/interview_analysis/interview_analysis/scripts/assessment/models/' + filename
	with open(path,'rb') as f:
    	clf = pickle.load(f)
    return clf

def predict(feature_name, x):
	""" 
	Loads a classifier and makes a prediction. Retruns true if the prediction is 1
	"""
	clf = load_model(feature_name)
	return clf.predict(x) is 1

