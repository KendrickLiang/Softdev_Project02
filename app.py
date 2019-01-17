import json, urllib, os

from flask import Flask, render_template, flash, request, session, redirect, url_for

from util import db as silo
from util import farm
from util import api

silo.fileName("data/silo.db")
silo.createTables()
app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route("/")
def index():
    if 'current_user' in session:
        #print(not silo.haveFarm(session['current_user']))
        if not silo.haveFarm(session['current_user']):
            return render_template('home.html', noFarm=True, cash = silo.getCash(session['current_user']), cropTypes="")
        else:
            return render_template('home.html',
                farm=silo.getFarm(session['current_user'], silo.getFarmName(session['current_user'])[0][0]),
                cash = silo.getCash(session['current_user']),
                message='WELCOME '+  silo.getFarmName(session['current_user'])[0][0] + session['current_user'] ,
                noFarm=False,
                cropTypes = api.getCropInfo())
    return render_template('login.html', title="Login")

@app.route("/authentication", methods=['POST'])
def authenticate():
    '''
    Checks if the user, password pair sent is valid
    If not sent them back to login page
    If valid - log them in and send them to the home page
    '''
    username, password = request.form['username'].strip(), request.form['password'].strip()
    if username != '' and password != ''  and silo.checkUser(username, password):
        session['current_user'] = username
        current_user = username
    else:
        flash("Invalid Login")
    return redirect("/")

@app.route("/registration", methods=['POST'])
def register():
    '''
    Checks if the username sent is in database
    if Yes - redirect back to register page
    if No - add user, password into database and send them to the home page
    '''
    if silo.addUser(request.form['username'].strip(), request.form['password'].strip()):
        session['current_user'] = request.form['username']
        return redirect("/")
    flash("Invalid Username")
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop('current_user')
    return redirect("/")

@app.route("/viewprofile")
def view():
    return render_template('profile.html', user=session['current_user'], farm=silo.getFarmName(session['current_user']), crops=silo.getCrop(session['current_user']), land=silo.getLand(session['current_user']), cash=silo.getCash(session['current_user']))

@app.route("/location", methods=['POST'])
def createFarm():
    userInfo = [ request.form['farmName'], request.form['visible'] ]
    results = [ api.getipLocation(), api.searchLocation(request.form['location']) ]
    for row in results[1]:
        print(row)
    return render_template('location.html', userInput = userInfo, location_query = request.form['location'], location_result = results)

@app.route("/createFarm", methods=['POST'])
def locationSelection():
    farm.createFarm(session['current_user'], request.form['farmName'], request.form['location'],  100, request.form['visible'])
    return redirect("/")

@app.route("/plantInfo", methods=['POST'])
def plantInfo():
    print("HERE")
    models = api.getModels()
    cropID = request.form['cropID']
    print(cropID)
    for model in models:
        if cropID in model['_links']['awhere:crop'][0]['href']:
            link = model['_links']['self']['href']
    details = api.getModelDetails(link)
    #print(details)
    return json.dumps(details);

@app.route("/weatherInfo", methods=['POST'])
def weatherInfo():
    return json.dumps(api.weatherInfo(session['current_user'], silo.getFarmName(session['current_user'])))

@app.route("/updateCash", methods=['POST'])
def updateCash():
    silo.updateCash(request.form['cashNum'], session['current_user'])

@app.route("/updateMap", methods=['POST'])
def updateMap():
    silo.updateCrop(session['current_user'], silo.getFarmName(session['current_user'])[0][0], request.form['cropsMap'])
    silo.updateMap(session['current_user'], silo.getFarmName(session['current_user'])[0][0], request.form['map'])
    return ''

@app.route("/getCrop", methods=['POST'])
def getCropList():
    cropList = silo.getCrop(session['current_user'], silo.getFarmName(session['current_user'])[0][0])
    return json.dumps({'cropList': cropList})

if __name__ == "__main__":
    app.debug = True
    app.run()
