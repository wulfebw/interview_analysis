"""
filename: linguistic_analysis.py 
description: The functions in this file do the following:

	- recognize speech from an audio file
	- analyze language in text format 
		- get most common word
		- get most common bigram
		- get number of times a specific word was said

"""

import os
import sys
import nltk
import sphinxbase
import pocketsphinx

"""
Recognize Speech from audio files.
"""

def recognize_speech(filename,
					hmm = '/home/ec2-user/interview_analysis/speech_models/cmusphinx-5prealpha-en-us-2.0',
					lm = '/home/ec2-user/interview_analysis/speech_models/cmusphinx-5.0-en-us.lm.dmp',
					dic = '/home/ec2-user/interview_analysis/speech_models/hub4.5000.dic',
					samp_rate = '16000'):
	"""
	Recognizes speech in a wave file.

	:type hmm: string
	:param hmm: the hidden markov model file location

	:type lm: string
	:param lm: the language model file location

	:type dic: string
	:param dic: the dictionary file location

	:type samp_rate: string
	:param samp_rate: the sample rate at which the speech recognition models were trained

	:rtype: string
	:return: the speech in the provided audio file
	"""

	speech_recognizer = pocketsphinx.Decoder(hmm=hmm, lm=lm, dict=dic, samprate=samp_rate)
	# open the wave file
	wavfile = file(filename, 'r')
	wavfile.seek(50)
	# decode speech in the wave file
	speech_recognizer.decode_raw(wavfile)
	# return the hypothesis of the recognizer. 
	result = speech_recognizer.get_hyp()
	# actual result is a tuple and we only want the decoded speech (first element in tuple)
	return result[0]

"""
Extract speech features.
"""

def get_most_common_word(tokens):
	""" 
	Gets the most common word. 

	:type tokens: list of strings
	:param tokens: list of the words in speech

	:rtype: string
	:return: the most common word in the speech
	"""

	freq_dist = nltk.FreqDist(tokens)
	return freq_dist.most_common(1)

def get_most_common_bigram(tokens):
	""" 
	Gets the most common bigram. 

	:type tokens: list of strings
	:param tokens: list of the words in speech

	:rtype: string
	:return: the most common bigram in the speech
	"""

	bigrams = list(nltk.bigrams(tokens))
	freq_dist_bigrams = nltk.FreqDist(bigrams)
	return freq_dist_bigrams.most_common(1)

def get_num_occurences_of_word(tokens, word='i'):
	""" 
	Gets the number of occurences of a word, with default as 'I'. 

	:type tokens: list of strings
	:param tokens: list of the words in speech

	:type word: string
	:param word: the word to retrieve the count of
	"""
	
	return tokens.count(word)

def get_linguistic_features(speech):
	""" Calculates all linguistic features and then returns a dictionary of labels to features. """

	tokens = nltk.word_tokenize(speech)
	linguistic_features = dict()
	linguistic_features['speech'] = speech
	linguistic_features['most common word'] = get_most_common_word(tokens)
	linguistic_features['most common bigram'] = get_most_common_bigram(tokens)
	linguistic_features['number of occurences of {0}'.format('i')] = get_num_occurences_of_word(tokens, 'i')
	return linguistic_features 


if __name__ == "__main__":
	wavfile = "/home/ec2-user/flask_attempts/uploads/audio_test_1.wav"
	result = recognize_speech(wavfile)
	print(result) 
