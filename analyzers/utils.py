"""
filename: utils.py 
description: The functions in this file do the following:
	
	- convert between certain audio file formats
	- get the extension of a file
	- get the duration of a file (audio)

"""

import os
import sys
import wave
import random
import traceback
import subprocess

def exception_response(e):
	"""
	What is the correct thing to do with regards to logging info in a web app?
	"""

	raise Exception(e)

def get_file_ext(filename):
	"""
	Returns the extension of the given file.
	"""

	return filename.rsplit('.')[-1]

def allowed_file(filename):
	""" 
	For a given file, return whether it's an allowed type or not.
	"""

	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def new_filename(orig, to_add):
	"""
	Inserts a string into another string.
	"""

	new = orig.rsplit('.')
	new = new[:-1] + [to_add] + ['.'] + [new[-1]]
	return ''.join(new)

def get_rand_hex_value(n_digits):
	"""
	Returns a random hex string n_digits long.
	"""

	return '%0{0}x'.format(n_digits) % random.randrange(16**n_digits)

def make_dirs(pk, base='interviews'):
	"""
	Creates the directories used to stroe this video. This is awfully shortsighted to do all this 
	file stuff when I'm just going to use a database, but oh well.
	"""

	dirs = []
	interview_dir = base + '/' + pk
	dirs.append(interview_dir)
	uploads_dir = interview_dir + '/' + 'uploads'
	dirs.append(uploads_dir)
	features_dir = interview_dir + '/' + 'features'
	dirs.append(features_dir)
	linguistic_dir = features_dir + '/' + 'linguistic'
	dirs.append(linguistic_dir)
	paralinguistic_dir = features_dir + '/' + 'paralinguistic'
	dirs.append(paralinguistic_dir)
	visual_dir = features_dir + '/' + 'visual'
	dirs.append(visual_dir)

	for directory in dirs:
		if not os.path.exists(directory):
			os.makedirs(directory)


def stereo_to_mono(filename, samp_rate=16000, sox_exec_file='/usr/local/bin/sox'):
	"""
	Converts an audio file from stereo to mono as well as changing it's sample rate and speed
	"""
	rtn_filename = ''
	try:
		speed = 2.75625		# 44100 / 16000 // how to get sample rate instead of assuming it is 44100?
		rtn_filename = new_filename(filename, '_mono')
		call_str = "{4} -r {2} {0} {1} channels 1 speed {3}".format(filename, rtn_filename, samp_rate, speed, sox_exec_file)
		subprocess.call(call_str, shell=True, stderr=subprocess.STDOUT)
	except Exception as e:
		exception_response(e)
	return rtn_filename

def get_file_duration(filename):
	"""
	Returns the duration of a file. Currently implmented for wave files only.
	"""

	if get_file_ext(filename) is 'wav':
		framerate = 0
		n_frames = 0
		wavfile = wave.open(wavefile, 'rb')
		n_frames = wavfile.getnframes()
		samprate = wavfile.getframerate()
		duration = n_frames / samprate
		return int(duration)
	else:
		raise NotImplementedError("Only wave file durations are supported. ")

def write_dict_features_to_file(features, output_filename):
	"""
	Write features in the form of a dictionary to an output file.
	"""

	with open(output_filename, 'w') as f:
		for key, value in features.iteritems():
			f.write('{0} : {1}'.format(key, value))
		f.close()

if __name__ == "__main__":
	pk = get_rand_hex_value(10)
	make_dirs(pk)

