from flask.ext.sqlalchemy import SQLAlchemy
from upload_analysis import app, db
from config import DevelopmentConfig
from analyzers.utils import get_file_duration
from analyzers.linguistic_analysis import recognize_speech, get_most_common_word, get_most_common_bigram, get_num_occurences_of_word

class Interview(db.Model):
	__tablename__ = 'interviews'
	id = db.Column(db.Integer, primary_key=True)
	""" Meta features """
	hex_id = db.Column(db.String(app.config['HEX_PK_LENGTH']), nullable=False)
	duration = db.Column(db.Integer)
	""" Linguistic features """
	speech = db.Column(db.String(700))
	most_common_word = db.Column(db.String(app.Config['MAX_WORD_LENGTH']))
	most_common_bigram = db.Column(db.String(app.Config['MAX_WORD_LENGTH'] * 2))
	n_occurences_i = db.Column(db.Integer)

	def __init__(self, video_file, audio_file, hex_id):
		self.hex_id = hex_id

	def get_audio_filename(self):
		return app.Config['UPLOAD_FOLDER'] + self.hex_id + app.Config['AUDIO_FILENAME']

	def get_video_filename(self):
		return app.Config['UPLOAD_FOLDER'] + self.hex_id + app.Config['AUDIO_FILENAME']

	def extract_features(self):
		self.speech = recognize_speech(self.get_audio_filename())
		self.duration = get_file_duration(self.get_audio_filename())
		tokens = nltk.word_tokenize(speech)
		self.most_common_word = get_most_common_word(tokens)
		self.most_common_bigram = get_most_common_bigram(tokens)
		self.n_occurences_i = get_num_occurences_of_word(tokens, 'i')
