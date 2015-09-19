from flask import Flask, redirect, request, url_for
import os
from werkzeug import secure_filename
import notecv.findTones as cv
import cv2
import music.music_processing as mp
from datetime import datetime
from subprocess import call
import json
import random,string

UPLOAD_FOLDER = os.path.join('.', 'notecv', 'images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


melody = Flask(__name__)
melody.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@melody.route("/", methods=['GET'])
def app():
    return melody.send_static_file('index.html')

@melody.route("/upload/", methods=['POST'])
def upload():
    try:
        if request.method == 'POST':
            print dir(request)
            print 'data:{}'.format(request.data)
            name = random_name()
            image_path = save_image(name,request)
            image_data = do_cv(image_path)
            wav_path   = make_music(name,image_data)
            wav_path = url_for('static', filename=wav_path)
            return redirect(wav_path)
    except:
        import traceback,sys
        print (sys.exc_info()[0])
        traceback.print_tb(sys.exc_info()[2])
        return "Please upload a picture of your orange box."


def random_name():
    return ''.join(random.choice(string.ascii_uppercase +
                                 string.ascii_lowercase)
                   for _ in xrange(6))

# Save image to images folder and return path to that folder
def save_image(name,request):
    if request.method == 'POST':
        print request.form
        print request.files
        file = request.files['file']
        name = str(datetime.now()) + '.' + name + '.' + file.filename
        if file and allowed_file(name):
            filename = secure_filename(name)
            print filename
            path = os.path.join(melody.config['UPLOAD_FOLDER'], filename)
            print path
            file.save(path)
            return path

def do_cv(imgPath):
    img = cv2.imread(imgPath)
    return cv.processImage(img)[0]

def make_music(name,imgData):
    print "MAKING MUSIC"
    print imgData
    currDir = os.getcwd()
    os.chdir("./music")
    # imgData = json.loads(json.dumps(imgData))
    outname = name + '.wav'
    mp.main(imgData,outfile=outname)
    call(["mv", os.path.join('.',outname), "../static/"])
    os.chdir(currDir)
    return outname

# Return True if filename is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    melody.run(host='0.0.0.0',debug=True,port=80)

