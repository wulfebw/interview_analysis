from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.sqlalchemy import SQLAlchemy

#from analyzers.linguistic_analysis import recognize_speech, get_linguistic_features
from analyzers.utils import get_rand_hex_value, make_dirs, stereo_to_mono, write_dict_features_to_file

import logging
from logging.handlers import RotatingFileHandler

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask_test_db'
db = SQLAlchemy(app)

from models import Interview

# This is the path to the upload directory
# app.config['UPLOAD_FOLDER'] = 'interviews/'

# These are the extension that we are accepting to be uploaded
# app.config['ALLOWED_EXTENSIONS'] = set(['wav', 'webm'])

# Set the route to the file upload
@app.route('/')
def index():
    return render_template('recordrtc_index.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():

	# get a random value to indentify this interview
	# not using a database for now, really need to learn more flask
	pk_length = app.config['HEX_PK_LENGTH']
	pk = get_rand_hex_value(pk_length)
	make_dirs(pk)

	# create a dictionary to hold the features we collect
	rtn_features = dict()
	# init the audio and video files to be returned
	video_filename = ''
	audio_filename = ''

	# video upload
	try:
		video = request.files['video-blob']
	except Exception as e:
		video = None
		# raise Exception(e)

	if video:
		# dir/filename for video to be saved as
		video_filename = os.path.join(app.config['UPLOAD_FOLDER'],'{0}/uploads/video.webm'.format(pk))
		# set the filename link to send back to the user
		video_link = '{0}/uploads/video.webm'.format(pk)
		# save the video
		video.save(video_filename)

	try:
		audio = request.files['audio-blob']
	except Exception as e:
		audio = None
		# raise Exception(e)

	if audio:
		# dir/filename for audio to be saved as
		audio_filename = os.path.join(app.config['UPLOAD_FOLDER'],'{0}/uploads/audio.wav'.format(pk))
		# set the filename link to send back to the user
		audio_link = '{0}/uploads/audio.wav'.format(pk)
		# save the audio 
		audio.save(audio_filename)
		# convert to mono
		audio_mono_filename = stereo_to_mono(audio_filename)
		# perform speech recognition
		speech = 'test speech' #recognize_speech(audio_mono_filename)
		# get the linguistic stats 
		linguistic_features = {} #get_linguistic_features(speech)
		# get output file for linguistic features
		linguistic_features_file = 'interviews/{0}/features/linguistic_features.txt'.format(pk)
		# write linguistic features to file
		write_dict_features_to_file(linguistic_features, linguistic_features_file)
		# add linguistic features to rtn_dict
		rtn_features = dict(rtn_features.items() + linguistic_features.items())

	# render the template with the collected features
	return render_template('features.html', 
							features=rtn_features, 
							video_filename=video_filename, 
							audio_filename=audio_filename, 
							pk=pk)

# route that will display previously uploaded media
@app.route('/interviews/<path:filepath>')
def uploaded_file(filepath):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filepath)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
	app.run(debug=True)

