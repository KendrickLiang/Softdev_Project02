import json, urllib, os

from flask import Flask, render_template, flash, request, session, redirect, url_for

from util import db as silo

global DB_FIlE = "/data/silo.db"
app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route("/")
def index():
    print(session)
    if 'current_user' in session:
        return render_template('home.html', message='Your farm')
    return render_template('login.html', title="Login")

@app.route("/authentication", methods=['POST'])
def authenticate():
    '''
    Checks if the user, password pair sent is valid
    If not sent them back to login page
    If valid - log them in and send them to the home page
    '''
    username, password = request.form['username'].strip(), request.form['password'].strip()
    if username == '' and password == '':
        return redirect("/")
    if silo.checkUser(username, password):
        session['current_user'] = username
        current_user = username
        return redirect("/")
    return render_template('home.html', message='FAIL@')

@app.route("/registration", methods=['POST'])
def register():
    '''
    Checks if the username sent is in database
    if Yes - redirect back to register page
    if No - add user, password into database and send them to the home page
    '''
    if silo.addUser(request.form['username'].strip(), request.form['password'].strip()):
        session['current_user'] = username
        return render_template('home.html', message='WELCOME'+request.form['username'].strip())
    render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('current_user')
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()
