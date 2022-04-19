# # pip install tensorflow, keras, pickle, nltk,re
import nltk
from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# nltk.download('stopwords')
# stop_word = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
import json
import pickle
import tensorflow 
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random
import re



def cleaning(sentence):
    sentence= sentence.lower()
    sentence = re.sub(r"i'm","i am",sentence)
    sentence = re.sub(r"he's","he is",sentence)	
    sentence = re.sub(r"she's","she is",sentence)	
    sentence = re.sub(r"that's","that is",sentence)
    sentence = re.sub(r"what's","what is",sentence)	
    sentence = re.sub(r"where's","where is",sentence)		
    sentence = re.sub(r"\'ll","will",sentence)	
    sentence = re.sub(r"\'ve","have",sentence)	
    sentence = re.sub(r"\'re","are",sentence)	
    sentence = re.sub(r"\'d","will",sentence)	
    sentence = re.sub(r"won't","will not",sentence)	 
    sentence = re.sub(r"can't","cannot",sentence)	
    sentence = re.sub(r"[-()\"#/@;:<>=|.?,]","",sentence)
    return sentence
#--------------
words=[]
classes = []
documents = []   #=>(pattern[i],tag)
ignore_words = ['?', '!']
data_file = open('intents.json').read()
intents = json.loads(data_file)
#--------------
# stop_word=["a","the","an","c'mon","co","co.","t's","un","unto","v","viz","vs","a","b","c","d","e","f","g","h","j","l","m","n","o","p","q","r","s","t","u","uucp","w","x","y","z"]
for intent in intents['intents']:
    classes.append(intent['tag'])
    for pattern in intent['patterns']:
        #tokenize each word
        w = nltk.word_tokenize(cleaning(pattern))
        
        words.extend(w)
        #add documents in the corpus
        documents.append((w, intent['tag']))

            
#--------------------
# lemmatize, lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words]
words = sorted(list(set(words)))
# sort classes
classes = sorted(list(set(classes)))
# documents = combination between patterns and intents
# print (len(documents), "documents")
# # classes = intents
# print (len(classes), "classes", classes)
# # words = all words, vocabulary
# print (len(words), "unique lemmatized words", words)

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

#---------------------
# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(classes)
# training set, bag of words for each sentence
for doc in documents:  #D=(W,T)
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)  #=>inputs pattern

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1  #=>tag as output

    training.append([bag, output_row])
# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")
#--------------------------
# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.00087, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model 
hist = model.fit(np.array(train_x), np.array(train_y),epochs=1000, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)

print("model created")

