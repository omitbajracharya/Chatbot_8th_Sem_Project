###pip install nltk,tensorflow,keras,pickle,re,mysql.connector,numpy
from turtle import goto
import nltk
from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# stop_word =stopwords.words('english')
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import re
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
import mysql.connector

#Creating GUI with tkinter
# import tkinter
from tkinter import *
base = Tk()
name_var=StringVar()

# stop_word=["a","the","an","c'mon","co","co.","t's","un","unto","v","viz","vs","a","b","c","d","e","f","g","h","j","l","m","n","o","p","q","r","s","t","u","uucp","w","x","y","z"]
#--------
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
bot_name = "khec_Bot"

#--------

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
    sentence_words = nltk.word_tokenize(sentence)

    # filter_stopword=[t for t in sentence_words if t not in stop_word]
    filter_word = list(filter(lambda x: x in classes or words, sentence_words))
    print("###########_______###############---------------"+str(filter_word)+"______________##########################")
    return filter_word
#--------

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words=cleaning(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"+str(res)+"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    # ERROR_THRESHOLD = 0.20

    results = [[i,r] for i,r in enumerate(res)]     #=> results=[[i,r],[i,r]....]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)  # x=[i,r]

    print("========="+str(results[0])+"==============================================")
    print("========="+str(results[1])+"==============================================")
    print("========="+str(results[3])+"==============================================")

    return_list = []
    # print("****-----------------------"+classes[86]+"-----------------------********")
    return_list.append({"intent": classes[results[0][0]], "probability": str(results[0][1])})
    print("++++++++++++++++++++"+str(return_list)+"++++++++++++++++++++++++++") 
    print("++++++++++++++++++++"+str({"intent": classes[results[1][0]], "probability": str(results[1][1])})+"++++++++++++++++++++++++++") 
    print("++++++++++++++++++++"+str({"intent": classes[results[3][0]], "probability": str(results[3][1])})+"++++++++++++++++++++++++++") 

    # for r in results[0]:
    #     return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    # print("++++++++++++++++++++"+str(return_list)+"++++++++++++++++++++++++++")    
    return return_list
    
def getResponse(ints, intents_json,tagging=False):
    if tagging == True:
        tag = ints
    else:
        tag = ints[0]['intent']
    
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(text):  
    if text in classes:
        res = getResponse(text,intents,tagging=True)
        print("This is my response==================>"+str(res))
        return res
    # else:    
    #     filter_word = cleaning(text)
    #     for word in filter_word:
    #         if lemmatizer.lemmatize(word) in classes: 
    #             word = lemmatizer.lemmatize(word)
    #         if (word in classes) :
    #             print("This is my response==================>"+str(word))
    #             res = getResponse(word,intents,tagging=True)
    #             return res

    ints = predict_class(text, model)  #ints=[{'tags':"greeting",'probability':"ihidhi"}]
    # ints=>highest probability ==>tags,probability
    # print("-------------------------------------"+ str(type(ints[0]['probability']))+"-----------------------------------------")
    # print(ints[0])  #==>dicionary of pattern class with high probability
    prob=float(ints[0]['probability']) #filtering the highest
    print(type(prob))
    if prob > 0.77:
        res = getResponse(ints, intents)
    else:
        res="Hey, I'm only a bot, I need things simple.Could you please place query more detailly or Exclude slang words?,Thank you"  

        mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="chatbot")

        mycursor = mydb.cursor()
        mycursor.execute(f"select * from `new_query` where `Query`='{text}'")
        lst_cursor=list(mycursor)
        l=len(lst_cursor)
        

        if l!=0:
            print(lst_cursor[0][2])
            val=lst_cursor[0][2]+1
            print("updating...")
            print(val)
            mycursor = mydb.cursor()
            mycursor.execute(f"UPDATE `new_query` SET `freq`= {val} where `Query`='{text}'")
            mydb.commit()
        else:
            print("inserting...")
            mycursor = mydb.cursor()
            # SELECT * FROM `new_query` WHERE `query`='xyz'
            query = f"INSERT INTO `new_query` (`Query`) VALUES ('{text}')"
            mycursor.execute(query)
            mydb.commit()
        mydb.close()    
    return res

#--------#--------#--------#--------#--------#--------#--------


# -----------------
def send(*args):
    msg=name_var.get()
    # print(msg)
    # after leave(msg)

    EntryBox.delete(0, 'end')
    EntryBox.insert(0, '')                
  
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

# ----------------

# call function when we click on entry box
def click(*args):
    EntryBox.delete(0, 'end')



base.title(bot_name)
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

# #Create the box to enter message
# EntryBox = Text(base,bg="#ADD8E6",bd=0,width="29", height="5", font="Arial")
# #EntryBox.bind("<Return>", send)

#Create the box to enter message
EntryBox = Entry(base,textvariable = name_var,bg="#ADD8E6",bd=0,width="29", font="Arial")

# Add text in Entry box
EntryBox.insert(0, 'Place your Query here.... ')
EntryBox.pack()
# Use bind method
EntryBox.bind("<Button-1>", click)

#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=6, y=400, height=50, width=370)
SendButton.place(x=6, y=460, height=30, width=370)
base.bind('<Return>', send)   #if enter key is pressed call function
base.mainloop()
