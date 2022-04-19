import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="chatbot")
mycursor = mydb.cursor()
mycursor.execute(f"SELECT `id` FROM `new_user_regis` WHERE `email` = 'riyabudhathoki2@gmail.com'")
print((mycursor[0]))