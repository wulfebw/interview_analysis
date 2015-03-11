

class Config(object):
	DEBUG = False
	HEX_PK_LENGTH = 16
	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/flask_test_db'
	UPLOAD_FOLDER = 'interviews/'
	ALLOWED_EXTENSIONS = set(['wav', 'webm'])
	VIDEO_FILENAME = 'video.webm'
	AUDIO_FILENAME = 'audio.wav'
	MAX_WORD_LENGTH = 20
	

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	Debug = True
