import sqlite3

DB_FIlE = "../data/silo.db"

def createTables():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #Creating our tables in our database
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, cash REAL, friends TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS farms(owner TEXT, farm_name TEXT, location TEXT, area INT, start_time TEXT, crops TEXT, map TEXT, visible INT)")
    c.execute("CREATE TABLE IF NOT EXISTS trades(user TEXT, item TEXT, count INT, cost REAL)")
    db.commit()
    db.close()

def addUser(user, password):
    user_list = getUsers()
    if user in user_list:
        return False
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users values (?, ?, ?, ?)", (user, password, 0, ''))
    db.commit()
    db.close()
    return True

def checkUser(user, password):
    user_list = getUsers()
    if user in user_list:
        if user_list[user] == password:
            return True

    return False

def getUsers():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # Gets the list of users in database
    c.execute("SELECT usernames FROM users")
    user_list = c.fetchall()

    db.commit()
    db.close()
    return user_list
