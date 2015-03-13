import os
from flask.ext.sqlalchemy import SQLAlchemy
from interview_analysis import app, db
from config import DevelopmentConfig
from scripts.utils import get_file_duration
from scripts.feature_extraction import linguistic
from constants import *


class Interview(db.Model):
	__tablename__ = 'interviews'
	id = db.Column(db.Integer, primary_key=True)
	""" Meta features """
	hex_id = db.Column(db.String(HEX_PK_LENGTH), nullable=False)
	duration = db.Column(db.Integer)
	question = db.Column(db.String(MAX_QUESTION_LENGTH))
	""" Linguistic features """
	speech = db.Column(db.String(700))
	most_common_word = db.Column(db.String(MAX_WORD_LENGTH))
	most_common_bigram = db.Column(db.String(MAX_WORD_LENGTH * 2))
	n_occurences_i = db.Column(db.Integer)

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
		self.n_occurrences_i = linguistic.get_num_occurrences_of_word(tokens, 'i')

	def get_features(self):
		rtn_dict = dict()
		# Linguistic features
		rtn_dict[SPEECH] = self.speech
		rtn_dict[DURATION] = self.duration
		rtn_dict[MOST_COMMON_WORD] = self.most_common_word
		rtn_dict[MOST_COMMON_BIGRAM] = self.most_common_bigram
		rtn_dict[N_OCCURRENCES_I] = self.n_occurrences_i
		rtn_dict[QUESTION] = self.question

		return rtn_dict
