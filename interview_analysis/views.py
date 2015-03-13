import os
from shutil import move
import random

from flask import render_template, request, redirect, url_for, send_from_directory

from interview_analysis import app, db

from scripts.utils import get_rand_hex_value, make_dirs, stereo_to_mono, write_dict_features_to_file

from models import Interview

from constants import *

# Set the route to the file upload
@app.route('/')
def index():
	question = random.choice(INTERVIEW_QUESTIONS)
	return render_template('interview_analysis/upload.html', question=question)

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():

	# get a random value to indentify this interview
	# not using a database for now, really need to learn more flask
	pk_length = HEX_PK_LENGTH
	pk = get_rand_hex_value(pk_length)
	print("PK_PRINT: {}".format(pk))
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
		# set the filename link to send back to the user
		video_link = '{0}/{1}'.format(pk, app.config['VIDEO_FILENAME'])
		# dir/filename for video to be saved as
		video_filename = os.path.join(app.config['UPLOAD_DIR'], video_link)
		# save the video
		video.save(video_filename)

	try:
		audio = request.files['audio-blob']
	except Exception as e:
		audio = None
		# raise Exception(e)

	if audio:
		# set the filename link to send back to the user
		audio_link = '{0}/{1}'.format(pk, app.config['AUDIO_FILENAME'])
		# dir/filename for audio to be saved as
		audio_filename = os.path.join(app.config['UPLOAD_DIR'], audio_link)
		print("AUDIO_FILENAME: {}".format(audio_filename))
		# save the audio 
		audio.save(audio_filename)
		# convert to mono
		audio_mono_filename = stereo_to_mono(audio_filename)
		print("AUDIO_MONO_FILENAME: {}".format(audio_mono_filename))
		# overwrite the original file with the mono one
		move(audio_mono_filename, audio_filename)
		# create the object
		interview = Interview(pk)
		# set the question
		interview.question = request.form['question']
		# extract features
		interview.extract_features()
		# retrieve features
		rtn_features = interview.get_features()
		# save the interview
		db.session.add(interview)
		db.session.commit()
	# render the template with the collected features
	return render_template('interview_analysis/analysis.html', 
							features=rtn_features, 
							video_filename=video_link, 
							audio_filename=audio_link, 
							pk=pk)

# route that will display previously uploaded media
@app.route('/interviews/<path:filepath>')
def uploaded_file(filepath):
	return send_from_directory(app.config['UPLOAD_DIR'], filepath)