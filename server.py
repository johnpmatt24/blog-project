from flask_app import app

from flask_app.controllers import users, posts, messages # insert file here

if __name__ == "__main__":
    app.run(debug=True)