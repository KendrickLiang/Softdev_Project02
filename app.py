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
        print(not silo.haveFarm(session['current_user']))
        return render_template('home.html', farm=silo.getFarm(session['current_user']), message='WELCOME '+session['current_user'], noFarm=not silo.haveFarm(session['current_user']), cropTypes = api.getCropInfo())
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
    return render_template('profile.html', user=session['current_user'], farm=silo.getFarmName(session['current_user']), crops="Corn", land="9", cash="180")

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
    models = api.getModels()
    cropID = request.form['cropID']
    for model in models:
        if cropID in model['_links']['awhere:crop'][0]['href']:
            link = model['_links']['self']['href']
    details = api.getModelDetails(link)
    return ''

if __name__ == "__main__":
    app.debug = True
    app.run()
