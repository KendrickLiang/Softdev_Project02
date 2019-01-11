import sqlite3

def fileName(name):
    global DB_FILE
    DB_FILE = name

def createTables():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #Creating our tables in our database
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, cash REAL, friends TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS farms(owner TEXT, farm_name TEXT, location TEXT, area INT, start_time INT, crops TEXT, map BLOB, visible INT);")
    c.execute("CREATE TABLE IF NOT EXISTS trades(user TEXT, item TEXT, count INT, cost REAL);")
    db.commit()
    db.close()

def addUser(user, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT EXISTS (SELECT 1 FROM users where username = (?) );", (user,))
    if c.fetchone()[0]:
        return False
    c.execute("INSERT INTO users values (?, ?, ?, ?);", (user, password, 0, ''))
    db.commit()
    db.close()
    return True

def checkUser(user, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT EXISTS (SELECT 1 FROM users where username = (?) );", (user))
    if c.fetchone()[0]:
        c.execute("SELECT password FROM users where username = (?);", (user))
        if c.fetchone()[0] == password:
            db.commit()
            db.close()
            return True
    db.commit()
    db.close()
    return False

def addFarm(owner, name, location, area, time, map, visible):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    values = (owner, name, location, area, time, '', map, visible)
    c.execute("INSERT INTO farms values (?, ?, ?, ?, ?, ?, ?, ?);", values)
    db.commit()
    db.close()

def haveFarm(user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT EXISTS (SELECT 1 FROM farms where owner = (?) );", (user))
    if c.fetchone()[0]:
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def getFarm(user):
    if not haveFarm(user):
        return ''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT map FROM farms where owner = (?);", (user))
    farm = c.fetchone()[0].split(";")
    for num in range(len(farm)):
        farm[num] = farm[num].split(",")
    db.commit()
    db.close()
    return farm

def getFarmName(user):
    if not haveFarm(user):
        return ''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT farm_name FROM farms where owner = (?);", (user))
    farmname = c.fetchall()
    db.commit()
    db.close()
    return farmname
