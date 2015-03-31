
""" INTERVIEW """
"""
Meta variables
"""
HEX_PK_LENGTH = 16
MAX_WORD_LENGTH = 20
MAX_QUESTION_LENGTH = 150

"""
Meta features
"""
QUESTION = 'question'
DURATION = 'duration'


"""
Linguistic features
"""
SPEECH = 'speech'
MOST_COMMON_WORD = 'most_common_word'
MOST_COMMON_BIGRAM = 'most_common_bigram'
N_OCCURRENCES_I = 'n_occurrences_i'
QUESTION_WORDS_IN_RESPONSE = 'question_words_in_response'


"""
Interview questions
"""
INTERVIEW_QUESTIONS = [
		'Can you tell me a little about yourself?',
		'What are your greatest professional strengths?',
		'What do you consider to be your weaknesses?',
		'What is your greatest professional achievement?',
		'Tell me about a challenge or conflict you have faced, and how you dealt with it.',
		'Where do you see yourself in five years?',
		'What is your dream job?',
		'Tell me about a time you exercised leadership.',
		'How would your boss and co-workers describe you?',
		'How do you deal with pressure or stressful situations?',
		'What do you like to do outside of work?',
		'What were the responsibilities of your last position?',
		'Give me an example of a time that you felt you went above and beyond the call of duty at work.',
		'Can you describe a time when your work was criticized?',
		'What is your greatest failure, and what did you learn from it?'
		]

""" ASSESSMENT """

PREDICTION = 'prediction'
ACTUAL = 'actual'

""" Features """
CONFIDENCE = 'confidence'
ENGAGEMENT = 'engagement'
TEAM_PLAYER = 'team_player'

""" Classifier Settings """
C = 1 
GAMMA = .1 
WEIGHT = 'auto' # {1:7.5, 0:1} 
KERNEL = 'linear'