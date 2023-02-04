from bdb import effective
from distutils.errors import DistutilsFileError
from turtle import width
from flask import render_template
from flask import request
from flask import Flask, flash, request, redirect, url_for

import face_recognition

UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def ocr():
    if request.method == 'GET':
        return render_template(
            "ocr.html"
        )
    if request.method == 'POST':
        return "okay"
    else:
        return "another"

@app.route("/ocr", methods=['GET', 'POST'])
def fileupload():
    if request.method == 'GET':
        return "GET"
    if request.method == 'POST':
        if 'image_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image_file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save("static/uploads/" + file.filename)

        image_url = "static/uploads/" + file.filename

        picture_of_me = face_recognition.load_image_file("static/IMG_3465.JPG")
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

        # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

        unknown_picture = face_recognition.load_image_file(image_url)
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)

        if len(unknown_face_encoding) > 0:
            print(unknown_face_encoding)
        # Now we can see the two face encodings are of the same person with `compare_faces`!
            unknown_face_encoding = unknown_face_encoding[0]
            results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

            result_str = ""
            if results[0] == True:
                result_str = "Same People!!!"
            else:
                result_str = "Different People!!!"
        else:
            result_str = "Not recognition!"
        return render_template(
            "result.html",
            result_str = result_str,
            sample_img = "static/me.JPG",
            image_url=image_url
        )
    else:
        return "another"
