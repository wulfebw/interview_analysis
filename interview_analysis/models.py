import os
from flask.ext.sqlalchemy import SQLAlchemy
from interview_analysis import app, db
from config import DevelopmentConfig
from scripts.utils import get_file_duration
from scripts.feature_extraction import linguistic
from scripts.assessment import predict
from constants import *


class Interview(db.Model):
	__tablename__ = 'interview'
	id = db.Column(db.Integer, primary_key=True)
	""" Meta features """
	hex_id = db.Column(db.String(HEX_PK_LENGTH), nullable=False)
	duration = db.Column(db.Integer)
	question = db.Column(db.String(MAX_QUESTION_LENGTH))
	""" Linguistic features """
	speech = db.Column(db.String(700))
	most_common_word = db.Column(db.String(MAX_WORD_LENGTH))
	most_common_bigram = db.Column(db.String(MAX_WORD_LENGTH * 2))
	n_occurrences_i = db.Column(db.Integer)
	question_words_in_response = db.Column(db.Boolean)
	""" The assessments of the interview """
	assessments = db.relationship('Assessment', backref='interview',
                                lazy='dynamic')

	def __init__(self, hex_id):
		self.hex_id = hex_id

	def get_audio_filename(self):
		return os.path.join(app.config['UPLOAD_DIR'], self.hex_id, app.config['AUDIO_FILENAME'])

	def get_video_filename(self):
		return os.path.join(app.config['UPLOAD_DIR'], self.hex_id, app.config['VIDEO_FILENAME'])

	def extract_features(self):
		"""
		Extracts features, adding each to a dictionary to be returned
		"""
		rtn_dict = dict()
		self.speech = linguistic.recognize_speech(self.get_audio_filename())
		self.duration = get_file_duration(self.get_audio_filename())
		tokens = linguistic.get_tokens(self.speech)
		self.most_common_word = linguistic.get_most_common_word(tokens)
		self.most_common_bigram = linguistic.get_most_common_bigram(tokens)
		self.question_words_in_response = linguistic.are_question_words_in_response(tokens, self.question)
		self.n_occurrences_i = linguistic.get_num_occurrences_of_word(tokens, 'i')

	def get_speech(self):
		return self.speech

	def get_question(self):
		return self.question

	def get_features(self):
		""" 
		Returns a dict of features associated with this interview
		"""
		rtn_dict = dict()
		# Linguistic features
		rtn_dict[DURATION] = self.duration
		rtn_dict[QUESTION_WORDS_IN_RESPONSE] = self.question_words_in_response
		rtn_dict[N_OCCURRENCES_I] = self.n_occurrences_i

		return rtn_dict

	def get_features_as_list(self):
		features = [self.duration, self.question_words_in_response, self.n_occurrences_i]
		return features


class Assessment(db.Model):
	__tablename__ = 'assessment'
	id = db.Column(db.Integer, primary_key=True)
	""" The interview being assessed """
	interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))
	""" assessment type: whether this is an assessment predicted by a model (PREDICTION) or a labled, human assessment (ACTUAL) """
	assessment_type = db.Column(db.String(10))
	""" High-level traits of an assessment """
	confidence = db.Column(db.Boolean)
	engagement = db.Column(db.Boolean)
	team_player = db.Column(db.Boolean)
	""" The ultimate hiring decision true=hire, false=don't hire"""
	hiring_decision = db.Column(db.Boolean)

	def __init__(self, interview, assessment_type):
		self.interview_id = interview.id
		self.assessment_type = assessment_type

	def predict(self):
		if self.assessment_type == PREDICTION:
			interview = Interview.query.filter_by(id=self.interview_id).first()
			features = interview.get_features_as_list()
			self.confidence = predict.predict(CONFIDENCE, features)
			self.engagement = predict.predict(ENGAGEMENT, features)
			self.team_player = predict.predict(TEAM_PLAYER, features)

	def get_predictions(self):
		rtn_dict = dict()
		rtn_dict[CONFIDENCE] = self.confidence
		rtn_dict[ENGAGEMENT] = self.engagement
		rtn_dict[TEAM_PLAYER] = self.team_player
		return rtn_dict

	def make_hiring_decision(self):
		return self.confidence and self.engagement and self.team_player
			


