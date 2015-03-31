""" 
filename: train.py 
date: 3/13/15
description: This file contains methods for loading data from db, training models, and storing models

todo:
	train models for high-level features
		(1) load in all interviews that have an ACTUAL assessment associated with them
		(2) create array of features from the interviews along with the target value associated with the high-level feature currently being assessed
		(3) train a model on this data
		(4) store the model
	train models to predict hiring decisions
		(1) load in all ACTUAL assessments associated with interviews
		(2) if they have confidence, engagement, team_player populated, add to array of features:target
		(3) train a model
		(4) save the model
"""
import csv
import pickle
import numpy as np

from sklearn import preprocessing, svm


def load_csv(feature_name):
	"""
	Loads in a csv file and returns sample and target arrays
	"""
	filename = feature_name + '.csv'
	path = '/Users/wulfe/Dropbox/Start/flask/interview_analysis/interview_analysis/static/admin/train/' + filename
	data_list = []
	with open(path, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		feature_labels = reader.next()
		for row in reader:
			data_list.append(map(int, row))
	data = np.array(data_list)
	x = preprocessing.scale(data[:,:-1])
	y = data[:,-1]
	return x,y

def save_model(feature_name, model):
	filename = feature_name + '.p'
	path = '/Users/wulfe/Dropbox/Start/flask/interview_analysis/interview_analysis/scripts/assessment/models/' + filename
	with open(path, 'wb') as f:
		pickle.dump(model, f)

def train(feature_name):
	x,y = load_csv(feature_name)
	print("loaded data")
	clf = svm.SVC(kernel='linear', cache_size=512)
	clf.fit(x,y)
	print("fitted classifier")
	save_model(feature_name, clf)
	print("saved classifier")

if __name__ == '__main__':
	models = ['confidence', 'engagement', 'team_player']
	for m in models:
		train(m)


