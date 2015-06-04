from flask import Flask, render_template, request
from tellcore.telldus import TelldusCore
import datetime
import subprocess
import lifx
import time
import re
app = Flask(__name__)
core = TelldusCore()

lights = None
attempts = 10
while not lights and attempts:
    try:
        lights = lifx.Lifx()
    except Exception as err:
        attempts -= 1
        print err


# ------------------------------------------------
# FUNCTIONS
# ------------------------------------------------
def stereo_control(state):
    if state:
        core.devices()[1].turn_on()
    else:
        core.devices()[1].turn_off()

def light_control(state):
    if state:
        lights.on()
    else:
        lights.off()

def speech(message):
    googleSpeechURL = getGoogleSpeechURL(message)
    subprocess.call(['mplayer', googleSpeechURL])

def getGoogleSpeechURL(message):
    googleTranslateURL = "http://translate.google.com/translate_tts?tl=sv&q="
    googleTranslateURL += message
    return googleTranslateURL

# ------------------------------------------------
# PAGES
# ------------------------------------------------
@app.route("/")
def index():
    subprocess.Popen('/root/web/cyka/start_stream.sh', shell=True)
    return render_template('main.html')

@app.route("/stream/")
def stream():
    return render_template('stream.html')
# ------------------------------------------------
# REQUESTS
# ------------------------------------------------
@app.route("/_lights_control")
def light_request():
    state = request.args.get('state', 0, type=int)
    light_control(state)
    return "success"

@app.route("/_stereo_control")
def stereo_request():
    state = request.args.get('state', 0, type=int)
    stereo_control(state)
    return "success"

@app.route("/_speech")
def speech_request():
    message = request.args.get('message', 0, type=str)
    speech(message)
    return "success"

@app.route("/_home")
def home_request():
    state = request.args.get('state', 0, type=int)
    light_control(state)
    if state:
        stereo_control(state)
        time.sleep(10)
        speech("What's up nigga")
    else:
        speech("Where are you going? Please don't leave.")
        time.sleep(10)
        stereo_control(state)

    return "success"

# ------------------------------------------------
# 404
# ------------------------------------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# ------------------------------------------------
# MAIN
# ------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)