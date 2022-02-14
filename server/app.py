from crypt import methods
from flask import Flask
app = Flask(__name__)


""" Gets a list of the current blink cameras
"""
@app.route('/cameras', method='GET')
def cameras():
    return ['LivingRoom', 'Office']

""" Snaps a picture at the current time and saves it to local storage

Path Args:
    camera_name: The name of the camera to take a picture from.
"""
@app.route('/picture/<camera_name>', method='GET')
def picture():
    return 'picture'


 
""" Downloads videos from the specified camera

Path Args:
    camera_name: The name of the camera to take a picture from.

Query Params:
    since: The date to start downloading videos from.
"""
@app.route('/videos/<camera_name>', method="GET")
def videos():
    return ['video1', 'video2']

