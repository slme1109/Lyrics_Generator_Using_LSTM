import os
import numpy as np
from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
# disable tensorflow warnings
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
'''
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed
3 = INFO, WARNING, and ERROR messages are not printed
'''
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
plt.style.use('ggplot') # plot style
mpl.rcParams["font.size"] = 18 # font size
# plt.switch_backend('agg')



def generator(seed_text, tokenizer, max_input_length, output_length, model):

	ix2word = tokenizer.index_word
	generated_text = seed_text
	# generate a fixed number of words
	for _ in range(output_length):
		# encode the text as integer
		encoded = tokenizer.texts_to_sequences([seed_text])[0] # [0] removes list of list problem
		# pad or truncate text to the length that matches the trained model
		encoded = pad_sequences([encoded], maxlen=max_input_length, truncating='pre', value = 0.0)
		# predict from trained model, greedy search.
		y_ix = model.predict_classes(encoded, verbose=0)
		generated_text += ' '+ ix2word[y_ix[0]] # e.g. y_ix = [66]

	print('<=== Seed_text: {} ===>'.format(seed_text))
	print('<=== Generated_lyrics: {} ===>\n'.format(generated_text))


def loss_plot(loss_train, loss_test):
    
    plt.rcParams["axes.grid"] = True
    fig, ax = plt.subplots(figsize=(10,6))
    n = len(loss_train)
    xtcks = np.arange(1, n+1)
    ax.set_title('Learning Curve')
    ax.set_xlabel('Training epochs')
    ax.set_ylabel('Loss')
    ax.plot(xtcks, loss_train, label='Train')
    ax.plot(xtcks, loss_test, label='Test')
    ax.legend()
    plt.savefig('../images/lc_word.jpg')
    plt.show()



if __name__ == "__main__":

	# Generator
	model = load_model('save/model.h5')
	tokenizer = load(open('save/tokenizer.pkl', 'rb'))

	seed_text = 'who is really slim shady'
	generator(seed_text, tokenizer, 10, 10, model)

	seed_text = 'look i was gonna go easy on you'
	generator(seed_text, tokenizer, 10, 10, model)

	#############################################################################
    # plot losses
	loss_array = np.load('save/loss.npz')['loss']
	loss_train, loss_test = loss_array[0], loss_array[1]
	loss_plot(loss_train, loss_test)
