from flask import Flask, redirect, request, url_for
import os
from werkzeug import secure_filename
import cv.findTones


UPLOAD_FOLDER = os.path.join('.', 'cv', 'images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


melody = Flask(__name__)
melody.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@melody.route("/", methods=['GET', 'POST'])
def app():
    image_path = save_image(request)
    image_data = do_cv(image_path)
    mp3 = make_music(json_path)
    return redirect(url_for(mp3_path))


# Save image to images folder and return path to that folder
def save_image(request):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return path


# Return True if filename is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    melody.run(debug=True)