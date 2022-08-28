import json
import os
from sqlite import SqlLite
from detect import Algorithem
from flask import Flask, request, render_template, flash, redirect, jsonify, Response, session
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def getprofile(vehicleNumber):
    sql = SqlLite()
    conn = sql.Connect()
    sql.CreateVehicleTable()
    vehicleInfo = None
    try:
        with conn:
            cur = conn.cursor()
            cur.execute(
                'SELECT name,address,car_model,license_no FROM VehicleInfo WHERE license_no=?', (vehicleNumber,))

            vehicleInfo = cur.fetchone()
    except:
        conn.rollback()
        msg = "Error occurred"

    finally:
        conn.close()

    return vehicleInfo


@app.route('/')
def index():
    return render_template('auth.html')


@app.route('/auth')
def auth():
    return render_template("auth.html")


@app.route('/home', methods=["POST", "GET"])
def home():
    sql = SqlLite()
    conn = sql.Connect()
    sql.CreateUserTable()
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


@app.route('/upload', methods=["POST", "GET"])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
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
        # Upload file to database (defined uploaded folder in static path)
        filename = "browse-uploaded-image.jpg"
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(
            app.config['UPLOAD_FOLDER'], filename)
        img_file_path = session.get('uploaded_img_file_path', None)
        vehicleNumber = algo.Detect(filename)
        profile = None
        if vehicleNumber != None:
            number = ''.join(filter(str.isalnum, vehicleNumber))
            profile = getprofile(number)
        print(profile, "asdas")
    return render_template('index.html', number=vehicleNumber, vehicle_image=img_file_path, profile=profile)


@app.route('/info', methods=['GET'])
def info():
    args = request.args
    vehicleNumber = args.get('v_num', default="", type=str)
    if vehicleNumber == "":
        return render_template('info.html', info=None)

    vehicleNumber = ''.join(filter(str.isalnum, vehicleNumber))
    print(vehicleNumber)
    vehicleInfo = getprofile(vehicleNumber)
    return render_template('info.html', info=vehicleInfo)


@app.route('/live')
def Live():
    return render_template('live.html')


@app.route('/video_feed')
def video_feed():
    algo = Algorithem()
    output = algo.getCamera()

    # Video streaming route. Put this in the src attribute of an img tag
    # for i in output:
    #     res = Response(i, mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(output, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/processImage', methods=['GET', 'POST'])
def processImage():
    if request.method == 'POST':
        algo = Algorithem()
        # fs = request.files['snap'] # it raise error when there is no `snap` in form
        fs = request.files.get('snap')
        if fs:
            filename = secure_filename(fs.filename)
            filename = "camera-uploaded-image.jpg"
            print('filename:', filename)
            fs.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            vehicleNumber = algo.Detect(filename)
            print(vehicleNumber, 'here is result')
            # Create Dictionary
            response = {"vehicleNumber": vehicleNumber, "msg": "Got Snap!"}

            # Dictionary to JSON Object using dumps() method
            # Return JSON Object
            return json.dumps(response)
        else:
            response = {"vehicleNumber": vehicleNumber,
                        "msg": "You forgot Snap!"}

            return json.dumps(response)

    return json.dumps({"vehicleNumber": None, "msg": "Something wrong with us!"})


if __name__ == '__main__':
    app.run()
