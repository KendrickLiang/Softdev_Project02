import json, urllib, os

from flask import Flask, render_template, flash, request, session, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return 'blank'

if __name__ == "__main__":
    app.debug = True
    app.run()
