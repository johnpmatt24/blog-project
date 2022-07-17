from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for
import urllib.request
import os
from werkzeug.utils import secure_filename

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user, post, like, image

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS  # depending on the file name, this will return either .png, jpg, jpeg or gif


@app.route("/")
def main():
    return render_template("userLog.html")




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/uploadPic")
def upload():
    if "user_id" not in session:
        return redirect("/logout")
    image_data = {
        "user_id": session["user_id"],
    }
    return render_template("uploadPic.html", img = image.Image.get_user_image(image_data))


@app.route("/updatePic")
def update_photo():
    if "user_id" not in session:
        return redirect("/logout")
    return render_template("updatePhoto.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "id": session["user_id"],   # id will be the person in session/logged in
        
    }
    
    image_data = {
        "user_id": session["user_id"],
    }
    
    return render_template("dashboard.html", 
                            img = image.Image.get_user_image(image_data),
                            user = user.User.get_user(data),
                            allposts = post.Post.get_all_post_with_users(),
                            ) 



@app.route("/user/register", methods = ["POST"])
def registration():
    if user.User.is_valid(request.form):
        in_database = user.User.get_user_by_email(request.form)
        if in_database:
            flash("Email already taken")
            return redirect("/")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form["last_name"],
            "age" : int(request.form["age"]),
            "country" : request.form["country"],
            "email" : request.form["email"],
            "password" : pw_hash,
        }
        user_id = user.User.save(data) #returns an id when we create/save a user
        session["user_id"] = user_id
        flash("Registration Sucessful.")
        return redirect('/')
    else:
        return redirect("/")





@app.route("/user/login", methods = ["POST"])
def user_login():
    if user.User.valid(request.form):
        in_database = user.User.get_user_by_email(request.form)
        if not in_database:
            flash('Invalid Email/Password. Try Again')
            return redirect("/")
    
        if not bcrypt.check_password_hash(in_database.password, request.form['password']):
            flash('Invalid Email/Password. Try Again')
            return redirect("/")
    
        session['user_id'] = in_database.id
        return redirect("/uploadPic")
    else:
        return redirect("/")



@app.route("/add/like", methods = ["POST"])
def add_like():
    if "user_id" not in session:
        return redirect("/logout")
    in_database = like.Like.get_post_user_like(request.form)
    
    like_data = {
        "user_id" : request.form["user_id"],
        "post_id" : request.form["post_id"]
    }
    if not in_database:
        like.Like.add_like(like_data)
        return redirect("/dashboard")
    else:
        return redirect("/dashboard")


@app.route("/delete/like/<int:id>/<int:pid>")
def delete_like(id, pid):
    data = {
        "user_id": id,
        "post_id": pid
    }
    in_database = like.Like.get_post_user_like(data)
    if in_database:
        like.Like.delete_like(data)
        return redirect("/dashboard")
    else:
        return redirect("/dashboard")




@app.route("/add/image", methods = ["POST"])
def add_image():
    if "user_id" not in session:
        return redirect("/logout")
    
    if "file" not in request.files:
        flash("No file part") #ensures that an extension is selected eg .png or .jpg
        return redirect("/uploadPic")
    file = request.files["file"]
    if file.filename == "":  #ensures that the file is not empty
        flash("No image selected for uploading")  
        return redirect("/uploadPic")
    
    if file and allowed_file(file.filename):  #if a file is selected and it meets the .png, .jpeg, jpg or .gif requirements
        filename = secure_filename(file.filename) #allows the filename to be safely stored
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #this joins the file name and our upload folder together (our upload folder will be our static/img folder)
        
        data = {
            "file" : filename,
            "user_id": session["user_id"],
        }
        image.Image.add_image(data)
        flash("Image uploaded successfully")
        return redirect("/uploadPic")
    else:
        flash("Allowed image types are - png, jpg, jpeg, gif")
        return redirect("/uploadPic")


@app.route("/update/image", methods = ["POST"])
def update_image():
    if "user_id" not in session:
        return redirect("/logout")
    
    if "file" not in request.files:
        flash("No file part")
        return redirect("/updatePic")
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect("/updatePic")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        data = {
            "file" : filename,
            "user_id": session["user_id"],
        }
        image.Image.update_image(data)
        flash("Image uploaded successfully")
        return redirect("/updatePic")
    else:
        flash("Allowed image types are - png, jpg, jpeg, gif")
        return redirect("/updatePic")



@app.route("/network")
def myNetwork():
    if "user_id" not in session:
        return redirect("/logout")
    return render_template("myNetwork.html", users = user.User.get_all(),)