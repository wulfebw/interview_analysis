from upload_analysis import app
from flask.ext.sqlalchemy import SQLAlchemy
from upload_analysis import db
from config import DevelopmentConfig

class Interview(db.Model):
	__tablename__ = 'interviews'
	id = db.Column(db.Integer, primary_key=True)
	hex_id = db.Column(db.String(app.config['HEX_PK_LENGTH']), nullable=False)
	duration = db.Column(db.Integer)
	most_common_word = db.Column(db.String(20))
	most_common_bigram = db.Column(db.String(20))
	n_occurences_i = db.Column(db.Integer)

	def __init__(self):
		pass	

	def get_audio_file(self):
		pass

	def get_video_file(self):
		pass