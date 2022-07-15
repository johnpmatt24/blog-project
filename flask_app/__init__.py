from flask import Flask, session
app = Flask(__name__, static_url_path='/static')
app.secret_key = "shhhhhh"
UPLOAD_FOLDER = 'flask_app\static\img'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

