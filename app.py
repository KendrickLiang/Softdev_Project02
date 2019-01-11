import json, urllib, os

from flask import Flask, render_template, flash, request, session, redirect, url_for

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
    username, password = request.form['username'].strip(), request.form['password'].strip()
    if username == '' and password == '':
        return render_template('home.html', message='FAIL')
    if username == 'a':#in db:
        if password == 'a':#db.pass
            session['current_user'] = username
            current_user = username
            return redirect("/")
    return render_template('home.html', message='FAIL@')

@app.route("/registration", methods=['POST'])
def register():
        return ''

@app.route("/logout")
def logout():
    session.pop('current_user')
    return redirect("/")

@app.route("/farm")
def farm():
    return render_template('farm.html', name = 'Derek')
if __name__ == "__main__":
    app.debug = True
    app.run()
