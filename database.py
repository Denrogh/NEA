import hashlib
import sqlite3
import re
import random
from conversion import random_postfix, random_infix, check_infix, check_postfix, postfix_to_infix, infix_to_postfix
"""Initialising the Database + Commands for accessing and manipulating the database"""


def get_posts_UserQuestion():
    #Debug command to show entries in database
    connection = sqlite3.connect('Main.db')
    c = connection.cursor()
    with connection:
        c.execute('SELECT * FROM UserQuestion')
        print(c.fetchall())

def get_posts_users():
    #Debug command to show entries in database
    connection = sqlite3.connect('Main.db')
    c = connection.cursor()
    with connection:
        c.execute('SELECT * FROM users')
        print(c.fetchall())


def get_posts_questions():
    #Debug command to show entries in database
    connection = sqlite3.connect('Main.db')
    c = connection.cursor()
    with connection:
        c.execute('SELECT * FROM questions')
        print(c.fetchall())


def get_number_questions():
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = 'SELECT count(*) FROM questions'
    c.execute(query)
    results = str(c.fetchall())
    results = results[2:-3]
    return results

def get_userID(username):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = 'SELECT UserID FROM users WHERE username = ?' #Find UserID given a username (of current user)
    try:
        c.execute(query, (username,))
    except:
        print("An error has occurred, UserID could not be found")
        return None
    results = c.fetchall()
    if results:
        results = str(results)
        UserID = results[2]
        return UserID
    else:
        print("Error this user is not in the database")
        exit()

def get_QuestionID_post(postfix):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = 'SELECT QuestionID FROM questions WHERE postfix_expression = ?' #Gives QuestionID from postfix_expression
    try:
        c.execute(query, (postfix,))
    except:
        print("An error has occurred, QuestionID could not be found")
        return None
    results = c.fetchall()
    if results:
        results = str(results)
        QuestionID = results[2:4] #Isoltaes QuestionID
        if "," in QuestionID:
            QuestionID = results[2]
        return QuestionID
    else:
        print("Error this question is not in the database")
        exit()


def get_QuestionID_infix(infix):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = 'SELECT QuestionID FROM questions WHERE infix_expression = ?' #Gives QuestionID from infix_expression
    try:
        c.execute(query, (infix,))
    except:
        print("An error has occurred, QuestionID could not be found")
        return None
    results = c.fetchall()
    if results:
        results = str(results)
        QuestionID = results[2] #Isoltaes QuestionID in the results
        return QuestionID
    else:
        print("Error this expression is not in the database")
        exit()

def get_random_infix(UserID,QuestionNumber):
    running = True
    while running:
        id = random.randint(1,int(QuestionNumber)) #Random QuestionID
        with sqlite3.connect('Main.db') as db:
            c = db.cursor()
        queryCheck = 'SELECT Status FROM UserQuestion WHERE QuestionID = ? and UserID = ?'
        queryQuestion = 'SELECT infix_expression FROM questions WHERE QuestionID = ?'
        c.execute(queryCheck,([id,UserID]))
        done = str(c.fetchall())
        if "None" not in done:
            attempted = True
        else:
            attempted = False
        if attempted == False:
            try:
                c.execute(queryQuestion,([id]))
                running = False
            except:
                print("An error has occurred, ID misconfigured")
                return None
    results = str(c.fetchall())
    infix = results[3:-4] #Strip away punctuation
    return infix

def get_random_postfix(UserID,QuestionNumber):
    running = True
    while running:
        id = random.randint(1,int(QuestionNumber)) #Random QuestionID
        with sqlite3.connect('Main.db') as db:
            c = db.cursor()
        queryCheck = 'SELECT Status FROM UserQuestion WHERE QuestionID = ? and UserID = ?'
        queryQuestion = 'SELECT postfix_expression FROM questions WHERE QuestionID = ?'
        c.execute(queryCheck,([id,UserID]))
        done = str(c.fetchall())
        print(done)
        if "None" not in done:
            attempted = True
        else:
            attempted = False
        if attempted == False:
            try:
                c.execute(queryQuestion,([id]))
                running = False
            except:
                print("An error has occurred, ID misconfigured")
                return None
    results = str(c.fetchall())
    postfix = results[3:-4] #Strip away punctuation
    return postfix

def get_post_answer(postfix):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = 'SELECT infix_expression FROM questions WHERE postfix_expression = ?'
    try:
        c.execute(query, ([postfix]))
    except:
        print("An error has occured, no equivalent expresion found")
        return None
    results = str(c.fetchall())
    infix = results[3:-4]
    return infix

def get_infix_answer(infix):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = 'SELECT postfix_expression FROM questions WHERE infix_expression = ?'
    try:
        c.execute(query, [infix])
    except:
        print("An error has occurred, no equivalent expression found")
        return None
    results = str(c.fetchall())
    postfix = results[3:-4]
    return postfix


def initialize():
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
###Database Creation
    c.execute('''CREATE TABLE users
                 ([UserID] INTEGER PRIMARY KEY AUTOINCREMENT,
                 [username] TEXT,
                 [password] TEXT,
                 unique(username))''')

    c.execute('''CREATE TABLE questions
                 ([QuestionID] INTEGER PRIMARY KEY AUTOINCREMENT,
                 [postfix_expression] TEXT,
                 [infix_expression] TEXT,
                 unique(postfix_expression))''')

    c.execute('''CREATE TABLE UserQuestion
                  ([QuestionID] INTEGER ,
                  [UserID] INTEGER,
                  [Status] TEXT ,
                  FOREIGN KEY (UserID) REFERENCES users (UserID),
                  FOREIGN KEY (QuestionID) REFERENCES questions (QuestionID))''')
    initialize_questions()
    db.commit()
    db.close()

def initialize_questions():
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    postfix_array = random_postfix()  # random postfix questions
    infix_array = random_infix(postfix_array)  # random infix questions
    queryQuestions = '''INSERT INTO questions (postfix_expression,infix_expression) VALUES (?,?) '''
    QuestionIDs = []
    for i in range(0, len(postfix_array)):
        try:
            c.execute(queryQuestions, (postfix_array[i], infix_array[i]))
            QuestionIDs.append(c.lastrowid) #Gives the QuestionID corresponding to the added question
        except:
            print("There has been an issue in creating the database")
            exit()
    db.commit()
    db.close
    return QuestionIDs

def initialize_UserQuestion(UserID, QuestionIDArray):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = '''INSERT INTO UserQuestion (QuestionID, UserID, Status) VALUES (?,?,?)'''
    for QuestionID in QuestionIDArray:
            c.execute(query, [QuestionID,UserID,None])
    db.commit()
    db.close()

def update_status(QuestionID,UserID,Status):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    queryUpdate = '''UPDATE UserQuestion SET Status = ? WHERE QuestionID = ? and UserID = ?'''
    queryInsert = '''INSERT INTO UserQuestion (QuestionID, UserID, Status) VALUES (?,?,?)'''
    try:
        c.execute(queryUpdate,(Status,QuestionID,UserID)) #If the field is there to update update it
    except:
        c.execute(queryInsert, (QuestionID,UserID,Status)) #Overwise initialize a new field with the needed values
    db.commit()
    db.close()


def correct_answers(UserID):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = '''SELECT count(*) FROM UserQuestion WHERE UserID = ? and Status = ?'''
    try:
        c.execute(query, (UserID, True))  # Gets all the true entries.
    except:
        print("Error executing query, correct answers")
        exit()
    CorrectAnswers = str(c.fetchall())
    CorrectAnswers = CorrectAnswers[2]
    return CorrectAnswers

def incorrect_answers(UserID):
    with sqlite3.connect('Main.db') as db:
        c = db.cursor()
    query = '''SELECT count(*) FROM UserQuestion WHERE UserID = ? and Status = ?'''
    try:
        c.execute(query, (UserID, False))  # Gets all the true entries.
    except:
        print("Error executing query, incorrect answers")
        exit()
    IncorrectAnswers = str(c.fetchall())
    IncorrectAnswers = IncorrectAnswers[2]
    return IncorrectAnswers


def add_new_postfix(postfix,UserID):
    if check_postfix(postfix): #Valid postfix string
        with sqlite3.connect('Main.db') as db:
            c = db.cursor()
        queryQuestion = '''INSERT INTO questions (postfix_expression,infix_expression) VALUES (?,?)'''
        queryUserQuestion = '''INSERT INTO UserQuestion (QuestionID, UserID, Status) VALUES (?,?,?)'''
        try:
            c.execute(queryQuestion, (postfix, postfix_to_infix(postfix))) #Insert the postfix and infix equivalent
            QuestionID = c.lastrowid
            c.execute(queryUserQuestion, (QuestionID, UserID, None))
        except:
            return "There has been an error in adding this question"
        # adds a new field with None as the question has not yet been attempted
        db.commit()
        db.close()


def add_new_infix(infix,UserID):
    if check_postfix(infix):  # Valid postfix string
        with sqlite3.connect('Main.db') as db:
            c = db.cursor()
        queryQuestion = 'INSERT INTO questions (postfix_expression,infix_expression) VALUES (?,?)'
        queryUserQuestion = '''INSERT INTO UserQuestion (QuestionID, UserID, Status) VALUES (?,?,?)'''
        try:
            c.execute(queryQuestion, (infix, infix_to_postfix(infix)))  # Insert the postfix and infix equivalent
            QuestionID = c.lastrowid
            c.execute(queryUserQuestion, (QuestionID, UserID, None))
        except:
            return "There has been an error in adding this question"
        # adds a new field with None as the question has not yet been attempted
        db.commit()
        db.close()

def login(username,password):
    logged_in = False #The user is not logged in
    hpassword = hash_password(password) #Hashes the password
    while not logged_in: #If a user is not logged in
        with sqlite3.connect('Main.db') as db:
            c = db.cursor()
        query = 'SELECT * FROM users WHERE username = ? AND password = ?'
        c.execute(query, [username, hpassword]) #Searches the database for a user with that username and password hash
        results = c.fetchall()
        if results: #if there is a user
                logged_in = True
                return logged_in #Will return True
        else:
            return logged_in #Will return false

def sign_up(username,password):
    if credentials(username,password): #Checks to see if the username/password meet requirements
        hpassword = hash_password(password) #Hashes the password
        with sqlite3.connect('Main.db') as db:
            c = db.cursor()
        querySign = 'INSERT INTO users (username,password) VALUES (?,?)'
        try:
            c.execute(querySign, (username,hpassword)) #execute the query
        except sqlite3.IntegrityError: #The username is not unique
            print("Username is already in use please try another",username,"username is here")
            return False #A user has not been signed up
        db.commit()
        db.close()
        UserID = get_userID(username)
        initialize_UserQuestion(UserID)
        return True #A user has been signed up
    else:
        return False #A user has not been signed up

def credentials(username,password):
    regex = "(?=.*[#?!@$%^&*=+<>])"
    if len(username) > 15:
        return False
    elif len(password) < 7:
        return False
    elif not re.match(regex,password):
        return False
    else:
        return True #All tests have been passed

def credentials_error(username,password):
    #Mirrors the credential function and returns the error type
    regex = "(?=.*[#?!@$%^&*=+<>])"
    if len(username) > 15:
        return "Username too long"
    elif len(password) < 7:
        return "Password too short, please pick a longer password"
    elif not re.match(regex,password):
        return "Password does not contain one of #?!@$%^&*=+<>"
    else:
        return "Username is already in use, Choose another"

def hash_password(password):
    hash_pass = (hashlib.md5(password.encode()))
    hash_password = hash_pass.hexdigest() #gives hex, easier to store and test
    return hash_password




print(random_postfix())


#sign_up("testuser","pass12!")
#sign_up("seconduser",")
#get_posts_questions()
#get_posts_UserQuestion()
#add_new_postfix("45+72-*",5)
#print(get_number_questions())
#get_posts_users()
#print("[(1, '19+75*6+8/+', '(1+9)+(((7*5)+6)/8)'), (2, '74+71*3/-', '(7+4)-((7*1)/3)'), (3, '246+*', '2*(4+6)'), (4, '75*1+', '(7*5)+1'), (5, '7831/42-**+3*', '(7+(8*((3/1)*(4-2))))*3'), (6, '8937+*/1+', '(8/(9*(3+7)))+1'), (7, '80*7/', '(8*0)/7'), (8, '941*+', '9+(4*1)'), (9, '13*2/', '(1*3)/2'), (10, '37*4*', '(3*7)*4'), (11, '76+5-', '(7+6)-5'), (12, '681*/', '6/(8*1)'), (13, '408+-', '4-(0+8)'), (14, '795/+', '7+(9/5)'), (15, '37-3-', '(3-7)-3'), (16, '48+1/', '(4+8)/1'), (17, '44*1*', '(4*4)*1'), (18, '24*73-*', '(2*4)*(7-3)'), (19, '25+9+', '(2+5)+9'), (20, '77+9-', '(7+7)-9'), (21, '475+*5-', '(4*(7+5))-5'), (22, '007++3/1-', '((0+(0+7))/3)-1')]")
#print("[(1, 1, None), (2, 1, '0'), (3, 1, '1'), (4, 1, None), (5, 1, None), (6, 1, None), (7, 1, None), (8, 1, None), (9, 1, None), (10, 1, '0'), (11, 1, None), (12, 1, None), (13, 1, None), (14, 1, None), (15, 1, None), (16, 1, None), (17, 1, None), (18, 1, None), (19, 1, None), (20, 1, '1'), (21, 1, None), (22, 1, None), (1, 2, None), (2, 2, None), (3, 2, None), (4, 2, None), (5, 2, None), (6, 2, None), (7, 2, None), (8, 2, None), (9, 2, None), (10, 2, None), (11, 2, None), (12, 2, None), (13, 2, None), (14, 2, None), (15, 2, None), (16, 2, None), (17, 2, None), (18, 2, None), (19, 2, None), (20, 2, None)]")
#get_posts_UserQuestion()