# Importing necessary packages
import random
import smtplib
from tkinter import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import os
from tkinter import ttk, messagebox
from datetime import date
####################### Chatbot part imports ###################
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
from datetime import date, datetime
# import mysql.connector
################################################################


############################ Chatbot Section  ########################
#--------

def cleaning(sentence):
    global words
    global classes
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
    global words
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
    global block
    global emailid
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="chatbot")
    if tagging == True:
        tag = ints
    else:
        tag = ints[0]['intent']

    if tag == 'aganist':
        block=1        


    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(text):  
    global intents
    global classes
    global model
    global emailid
    emailLogin=emailid.get()
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
    if prob > 0.7775:
        res = getResponse(ints, intents)
    else:
        res="Hey, I'm only a bot, I need things simple.Could you please place query more detailly or Exclude slang words?,Thank you"  

        mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="chatbot")
        # print("xyyyzzz====",emailLogin)
        mycursor = mydb.cursor()
        mycursor.execute(f"select * from `new_query` where `Query`='{text}' AND `email`='{emailLogin}'")
        lst_cursor=list(mycursor)
        l=len(lst_cursor)
        
        # riyabudhathoki2@gmail.com
        # print(l)
        if l!=0:
            c=lst_cursor[0][5]
            prevDateQuery=str(lst_cursor[0][4])[:10]
            # print(prevDateQuery)
            # mycursor = mydb.cursor()
            # mycursor.execute(f"SELECT CURRENT_DATE")

            
            now = datetime.today()
            now=now.strftime("%Y-%m-%d %H:%M:%S")

            today = str(date.today())
            if prevDateQuery!=today:
                c=1  
                
                mycursor = mydb.cursor()
                mycursor.execute(f"UPDATE `new_query` SET `Entry_at`= '{now}',`counter`='{c}' WHERE `Query`='{text}' AND `email`='{emailLogin}'")
                mydb.commit()

            # print(today)
            # print(prevDateQuery==today)
            # print(lst_cursor[0][3])
            val=lst_cursor[0][3]
            if c==2:
                messagebox.showwarning("Warning", "We will go through this topic later on!!! So for today please procceed to ask other questions for other topic...OtherWise you will be block for today...")
            elif c==3:
                val+=1
                mycursor = mydb.cursor()
                mycursor.execute(f"UPDATE `new_query` SET `counter`= '0' WHERE `Query`='{text}' AND `email`='{emailLogin}'")
                mydb.commit()
                
                mycursor = mydb.cursor()
                mycursor.execute(f"UPDATE `new_user_regis` SET `status`= 0, `time`='{now}' where `email`='{emailLogin}'")
                mydb.commit()


                base.destroy()
                messagebox.showerror("Blocked!!!", "*For Today, You have been block by admin...")
                main_account_screen()
                
            val+=1
            c+=1
            mycursor = mydb.cursor()
            mycursor.execute(f"UPDATE `new_query` SET `counter`='{c}' WHERE `Query`='{text}' AND `email`='{emailLogin}'")
            mydb.commit()

            print("updating...")
            print("Updated value is::",val,type(val))
            mycursor = mydb.cursor()
            mycursor.execute(f"UPDATE `new_query` SET `freq`= {val} where `Query`='{text}' AND `email`='{emailLogin}'")
            mydb.commit()
            
        else:
            print("inserting...")
            mycursor = mydb.cursor()
            # SELECT * FROM `new_query` WHERE `query`='xyz'
            query = f"INSERT INTO `new_query` (`email`,`Query`) VALUES ('{emailLogin}','{text}')"
            mycursor.execute(query)
            mydb.commit()
        mydb.close()    
    return res

#--------#--------#--------#--------#--------#--------#--------


# -----------------
def send(*args):
    global name_var
    global EntryBox
    global ChatLog
    global block
    global emailid
    msg=name_var.get()

    # print(msg)
    # after leave(msg)

    EntryBox.delete(0, 'end')
    EntryBox.insert(0, '')                
    

    global emailid
    emailVal=emailid.get()



    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        if block==1:
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="chatbot")
            mycursor = mydb.cursor()
            mycursor.execute(f"UPDATE `new_user_regis` SET `block`= '1' WHERE `email`='{emailid}'")
            mydb.commit()
            messagebox.showinfo("BLOCKED!!!", "Don't use slang words... So for now you have been blocked. visit college & lets discuss your problem...")
            base.destroy()
            main_account_screen()
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


# ----------------

# call function when we click on entry box
def click(*args):
    global EntryBox
    EntryBox.delete(0, 'end')

def chatbot(*args):
    global base
    global name_var
    global EntryBox
    global intents
    global words    
    global ChatLog
    global classes
    global emailid
    emailVal=emailid.get()
    global model

    base = Tk()
    name_var=StringVar()
    
    # stop_word=["a","the","an","c'mon","co","co.","t's","un","unto","v","viz","vs","a","b","c","d","e","f","g","h","j","l","m","n","o","p","q","r","s","t","u","uucp","w","x","y","z"]
    #--------
    intents = json.loads(open('intents.json').read())
    words = pickle.load(open('words.pkl','rb'))
    classes = pickle.load(open('classes.pkl','rb'))
    bot_name = "khec_Bot"
    #--------
    
    base.title(bot_name)
    base.geometry("400x500")
    base.resizable(width=FALSE, height=FALSE)

    #Create Chat window
    ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
    ChatLog.insert(END, "🖤🖤🖤 Welcome " + emailVal[:-10] + '🖤🖤🖤\n\n')

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

###########################  Chatbot Section ends here...........!!!  #####################################


def Authenticate(*args):
    global root
    global emailid
    global msgLabel
    global base
    emailVal=emailid.get()
    print(emailVal)
    if emailVal=="Place your registered email...":
        msgLabel.config(text = "*email???",foreground = "Red",font=('Helveticabold',13))
    else:
        print("***",emailVal,"***")
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="chatbot")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM `new_user_regis` WHERE `email` = '{emailVal}'")
        list1=list(mycursor)
    
        
    
        if list1[0][4]==0:    #not block then go to other process
            if len(list1)!=0:   #email register is there...it may have status 0 or 1
                # print("----------status:",list1[0][2],type(list1[0][2]))
                status=list1[0][2]
                mycursor = mydb.cursor()
                mycursor.execute(f"UPDATE `new_query` SET `counter`= 0 WHERE `counter`>=4")
                mydb.commit()
                if status==0:  #status==0
                    now = str(date.today())
                    prev=str(list1[0][3])[:10]
                    root.destroy()
                    if now!=prev:
                        ###################
                        now=date.today()
                        now=now.strftime("%Y-%m-%d %H:%M:%S")
                        mycursor = mydb.cursor()
                        mycursor.execute(f"UPDATE `new_user_regis` SET `status`= 1,`time`='{now}' WHERE `email`='{emailVal}'")
                        mydb.commit()
                        chatbot()
                        # print("***",emailVal,"***nepal***")            
                    else:
                        # msgLabel.config(text = "*This email is block by admin...",foreground = "Red",font=('Helveticabold',13))
                        messagebox.showerror("Blocked As Spammer!!!", "*This email is block for today <-- (Admin)")
                        main_account_screen()
                else:    #status==1
                    #successful login
                    root.destroy()
                    chatbot()
                # os.system('python chatbot.py')
            else:
                # messagebox.showerror("Error", "Please enter valid email address.")
                # Displaying the success message
                msgLabel.config(text = "*This email is not registered yet.",foreground = "Red",font=('Helveticabold',13))
        else:
            messagebox.showerror("Blocked For Slang words!!!", "*You have been blocked...Please visit college for discussion of your problem & solve all the misunderstanding...")
# def Registration(*args):
#     # print("Nepal")
#     global root
#     root.destroy()
#     os.system('python emailValidate.py')


    # ID = list(mycursor)[0][0]
    # print(ID)
        
def removePlaceholderOfemailEntry(*args):
    global emailEntry
    emailEntry.delete(0, 'end')
    emailEntry.config(fg="black")






def login(*args):
    global root
    global emailEntry
    global emailid
    global msgLabel
    
    # delete_register()
    # root = Toplevel(main_screen)
    
    # delete_mainscreen()
    
    
    # Creating object of tk class  
    root = Tk()

    # Setting the title, background color and disabling the resizing property
    root.geometry("500x200")
    root.title("Khec Login")
    root.resizable(False, False)
    root.config(background = "deepskyblue3")

    emailid = StringVar()
    emailLabel = Label(root, text="EMAIL-ID : ", bg="deepskyblue3",font=('Helveticabold',16))
    emailLabel.grid(row=0, column=1, padx=5, pady=20)

    emailEntry = Entry(root,textvariable=emailid, width=30,font=('Helveticabold',16),fg="#D2D2D2")
    emailEntry.grid(row=0, column=2, padx=5, pady=5)
    emailEntry.insert(0, 'Place your registered email...')
    

    # Use bind method
    emailEntry.bind("<Button-1>", removePlaceholderOfemailEntry)

    msgLabel = Label(root, bg="deepskyblue3")   
    msgLabel.place(x=50,y=50)

    loginbutton = Button(root, text="Login", command=Authenticate, width=30,font=('Helveticabold',18),fg="white",bg="green")
    loginbutton.place(x=60,y=100)
    root.bind('<Return>', Authenticate)   #if enter key is pressed call function
    # loginbutton.grid(row=4, column=2, padx=5, pady=5)

    # registerbutton =Button(root, text="Register", command=Registration, width=20,bg="deepskyblue3",foreground="red")
    # registerbutton.pack()
    # registerbutton.grid(row=5, column=2, padx=5, pady=5)
    link = Label(root, text="Not yet Register?SignUP",font=('Helveticabold',13), fg="white", cursor="hand2", bg="deepskyblue3")
    link.bind("<Button-1>",delete_login)
    link.place(x=180,y=150)
    root.mainloop()
  


 ################################  Registration  ######################################## 
# Defining CreateWidgets() function to create necessary tkinter widgets
def CreateWidget():
    global Email
    global regis
    global email_name
    global otp
    # Creating tkinter variables
    email_name = StringVar()
    otp = StringVar()

    emailLabel = Label(regis, text="ENTER YOUR EMAIL-ID : ", bg="deepskyblue3")
    emailLabel.grid(row=0, column=1, padx=5, pady=5)

    emailEntry = Entry(regis, textvariable=email_name, width=30)
    emailEntry.grid(row=0, column=2, padx=5, pady=5)

    sendOTPbutton = Button(regis, text="Send OTP", command=sendOTP, width=20)
    sendOTPbutton.grid(row=0, column=3, padx=5, pady=5)

    regis.msgLabel = Label(regis, bg="deepskyblue3")
    regis.msgLabel.grid(row=1, column=1, padx=5, pady=5, columnspan=3)

    otpLabel = Label(regis, text="ENTER THE OTP : ", bg="deepskyblue3")
    otpLabel.grid(row=2, column=1, padx=5, pady=5)

    regis.otpEntry = Entry(regis, textvariable=otp, width=30, show="*")
    regis.otpEntry.grid(row=2, column=2, padx=5, pady=5)

    validOTPbutton = Button(regis, text="Validate OTP", command=validOTP, width=20)
    validOTPbutton.grid(row=2, column=3, padx=5, pady=5)

    regis.otpLabel = Label(regis, bg="deepskyblue3")
    regis.otpLabel.grid(row=3, column=1, padx=5, pady=5, columnspan=3)
    link = Label(regis, text="Already have account?Login",font=('Helveticabold',13), fg="red", cursor="hand2", bg="deepskyblue3")
    link.bind("<Button-1>",delete_register)
    link.place(x=80,y=130)


# Defining sendOTP() to generate and send OTP to user-input email-id
def sendOTP():
    global regis
    global Email
    global email_name
    # Storing digits from 0 to 9 as string in numbers variable & declaring empty string
    # variable named root.genOTP
    numbers = "0123456789"
    regis.genOTP = ""
    # Fetching and storing user-input mail id in receiverEmail variable
    receiverEmail = email_name.get()
    Email=receiverEmail

    # Generating 6-digits OTP
    for i in range(6):
        regis.genOTP += numbers[int(random.random() * 10)]
    # Concatenating and Storing generated OTP with Message to be sent in otpMSG
    otpMSG = "YOUR OTP IS : " + regis.genOTP

    # Creating instance of class MIMEMultipart()
    message = MIMEMultipart()
    # Storing the email details in respective fields
    message['FROM'] = "OTP VALIDATOR (python_scripts)"
    message['To'] = receiverEmail
    message['Subject'] = "OTP VALIDATION"
    # Attaching the otgMSG with MIME instance
    message.attach(MIMEText(otpMSG))

  # Creating a smtp session
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # Starting TLS for security
    smtp.starttls()
    # Authenticating the sender using the login() method
    smtp.login("omitbajracharya55@gmail.com", "khec_chatbot")
    # Sending the email with Mulitpart message converted into string
    smtp.sendmail("omitbajracharya55@gmail.com", receiverEmail, message.as_string())
    # Terminating the session
    smtp.quit()

    # Formatting receiveEmail to replace(hide) mail id with *
    receiverEmail = '{}********{}'.format(receiverEmail[0:2], receiverEmail[-10:])
    # Displaying the success message
    regis.msgLabel.config(text = "OTP HAS BEEN SENT TO " + receiverEmail)

# Defining validOTP() to validate user-input OTP mail with script generated OTP
def validOTP():
    global otp
    global regis
    global email_name
    global Email
    global ID
    # Storing user-input OTP
    userInputOTP = otp.get()
    # Storing system generated OTP
    systemOTP = regis.genOTP

    # Validating OTP
    if userInputOTP == systemOTP:
        regis.otpLabel.config(text="OTP VALIDATED SUCCESSFULLY")
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="chatbot")
        mycursor = mydb.cursor()
        mycursor.execute(f"INSERT INTO `new_user_regis`(`email`) VALUES ('{Email}')")
        mydb.commit()
        messagebox.showinfo("💟💟Successfully Registered💟💟", "You have been Successfully registered to our system. Now You can join us with this email Id!!!")
        regis.destroy()
        login()
        # mycursor.execute(f"SELECT `id` FROM `new_user_regis` WHERE `email` = 'riyabudhathoki2@gmail.com'")
        # ID = list(mycursor)[0][0]
        # print(ID)
       # db....
        #user->id,email,status
        #login...
        #enter your email....email->status---your are block....no email ->register...select-email with status 1->welcome....chatpage
    else:
        regis.otpLabel.config(text="*INVALID OTP",fg="red")


def register(*args):
    # global root
    global regis
    # root.destroy()

    regis = Tk()
    # Setting the title, background color and disabling the resizing property
    regis.geometry("500x160")
    regis.title("Khec Validation")
    regis.resizable(False, False)
    regis.config(background = "deepskyblue3")

    # Calling the CreateWidgets() function with argument bgColor
    CreateWidget()

    # Defining infinite loop to run application
    regis.mainloop()


######################################   Registration code upto here...   ####################################





# Designing Main(first) window
 
def main_account_screen():
    global block
    block=0
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = delete_mainscreen_forLogin).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=delete_mainscreen_forRegister).pack()
 
    main_screen.mainloop()

 ############################################################################
def delete_mainscreen_forLogin(*args):
    global main_screen
    main_screen.destroy()
    login()

def delete_mainscreen_forRegister(*args):
    global main_screen
    main_screen.destroy()
    register()

def delete_login(*args):
    global root
    root.destroy()
    register()

def delete_register(*args):
    global regis
    regis.destroy()  
    login()      
 # ################################################################################### 
main_account_screen() 
