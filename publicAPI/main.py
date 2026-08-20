from flask import Flask
import os
import subprocess

pythonPath = os.path.join(os.getcwd(), '..', 'venv', 'bin', 'python3')
eventScript = os.path.join(os.getcwd(), '..', 'eventTracker.py')
appDir = os.path.join(os.getcwd(), '..')

app = Flask(__name__)

@app.route('/event/<event>')
def createEvent(event):
	subprocess.run([pythonPath, eventScript, event], cwd=appDir)
	return "event created"

app.run(port=5002)
