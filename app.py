from http.client import OK
import json
from flask import Flask, request, render_template, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from detect import Algorithem
from sqlite import SqlLite


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('auth.html')


@app.route('/auth')
def auth():
    return render_template("auth.html")


@app.route('/login', methods=["POST"])
def login():
    sql = SqlLite()
    conn = sql.Connect()
    user = None
    if request.method == 'POST':
        try:
            email = request.form['email']
            pswd = request.form['pswd']
            with conn:
                cur = conn.cursor()
                cur.execute(
                    'SELECT * FROM users WHERE email =? AND password=?', (email, pswd))
                user = cur.fetchone()
                msg = "Success"
        except:
            conn.rollback()
            msg = "Error occurred"

        finally:
            conn.close()
        if user != None:
            return render_template("index.html")
    return redirect(request.referrer)


@app.route('/register', methods=["POST"])
def register():
    sql = SqlLite()
    conn = sql.Connect()
    if request.method == 'POST':
        try:
            name = request.form['txt']
            email = request.form['email']
            pswd = request.form['pswd']
            with conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users(name, email, password) VALUES(?, ?, ?)", (name, email, pswd))

                conn.commit()
                msg = "Success"
        except:
            conn.rollback()
            msg = "Error occurred"

        finally:
            conn.close()
            return render_template("auth.html", msg=msg)


@app.route('/upload', methods=["POST"])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        algo = Algorithem()
    if file and algo.AllowedFile(file.filename):
        filename = secure_filename(file.filename)
        vehicelNumber = algo.Detect(filename)

    return render_template('index.html', number=vehicelNumber)


if __name__ == '__main__':
    app.run()
