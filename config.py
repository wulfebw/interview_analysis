import os

# Need to figure out the config.from_object method, but for now, global I guess:
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 	# gives: /Users/wulfe/Dropbox/Start/flask/interview_analysis
UPLOAD_DIR = BASE_DIR + '/interview_analysis/media/interviews'
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/flask_test_db'
ALLOWED_EXTENSIONS = set(['wav', 'webm'])
VIDEO_FILENAME = 'video.webm'
AUDIO_FILENAME = 'audio.wav'
# end global

class Config(object):
	DEBUG = False
	HEX_PK_LENGTH = 16
	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/flask_test_db'
	UPLOAD_FOLDER = 'media/interviews/'
	ALLOWED_EXTENSIONS = set(['wav', 'webm'])
	VIDEO_FILENAME = 'video.webm'
	AUDIO_FILENAME = 'audio.wav'
	MAX_WORD_LENGTH = 20
	

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	Debug = True
