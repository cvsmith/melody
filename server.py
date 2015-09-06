from flask import Flask, redirect, request, url_for
import os
from werkzeug import secure_filename
import notecv.findTones as cv
import cv2
import music.music_processing as mp
from datetime import datetime
from subprocess import call
from twilio import twiml
import urllib
import time
import json

UPLOAD_FOLDER = os.path.join('.', 'notecv', 'images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


melody = Flask(__name__)
melody.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@melody.route("/sms", methods=['POST'])
def sms():
    response = twiml.Response()
    
    if request.form['NumMedia'] != '0':
        image_path = save_image_sms(request.form['MediaUrl0'])
        print "Saved image"
        image_data = do_cv(image_path)
        print "Anaylzed image"
        wav_path = make_music(image_data)
        print "Made music"
        wav_path = url_for('static', filename='output.wav')
        response.message(url_for(wav_path))
    else:
        response.message("Could not find an image in your message.")
 
    return str(response)

# Save image to images folder and return path to that folder
def save_image_sms(media):
    print "first"
    print media
    filename = os.path.join(melody.config['UPLOAD_FOLDER'],
            str(time.time()) + '.jpg')
    print filename
    urllib.urlretrieve(media, filename) 
    print "got file"
    return filename

def do_cv(imgPath):
    img = cv2.imread(imgPath)
    return cv.processImage(img)[0]

def make_music(imgData):
    print imgData
    currDir = os.getcwd()
    os.chdir("./music")
    # imgData = json.loads(json.dumps(imgData))
    mp.main(imgData)
    call(["mv", "./output.wav", "../static/"])
    os.chdir(currDir)
    return "./static/output.wav"

# Return True if filename is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    melody.run(host='0.0.0.0',debug=True,port=80)

