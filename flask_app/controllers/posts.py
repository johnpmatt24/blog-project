from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import post, like, user, comment, image
# import urllib.request
# import os
# from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create/post', methods = ["POST"])
def create_post():
    if "user_id" not in session:
        return redirect("/logout")
    if post.Post.is_valid(request.form):
        data = {
            "title": request.form['title'],
            "content" : request.form['content'],
            "user_id": request.form["user_id"],
            "image_id": request.form["image_id"],
        }
        post.Post.save(data)
        return redirect("/dashboard")
    else:
        return redirect("/dashboard")


@app.route('/update/post', methods = ["POST"])
def update_post():
    if "user_id" not in session:
        return redirect("/logout")
    if post.Post.is_valid(request.form):
        data = {
            "pid": request.form["pid"],
            "title": request.form['title'],
            "content" : request.form['content'],
        }
        post.Post.update_post(data)
        return redirect("/dashboard")
    else:
        return redirect(f"/edit/post/{request.form['pid']}")




@app.route("/view/post/<int:pid>")
def view_post(pid):
    if "user_id" not in session:
        return redirect("/logout")
    
    user_data = {
        "id" : session["user_id"]
    }
    
    
    data = {
        "pid" : pid
    }
    
    
    like_data = {
        "post_id" : pid
    }
    
    image_data = {
        "user_id": session["user_id"],
    }
    
    img = image.Image.get_user_image(image_data)
    print(img.file)
    return render_template("viewPost.html",
                            img = img,
                            user = user.User.get_user(user_data), 
                            one_post = post.Post.get_post(data), 
                            postlikes = like.Like.get_posts_likes(like_data),
                            postcomments = comment.Comment.get_posts_comments(like_data)
                            )


@app.route("/edit/post/<int:pid>")
def edit_post(pid):
    if "user_id" not in session:
        return redirect("/logout")
    
    user_data = {
        "id" : session["user_id"]
    }
    
    data = {
        "pid": pid
    }
    return render_template("updatePost.html",
                            user = user.User.get_user(user_data),
                            one_post = post.Post.get_post(data))

@app.route("/delete/post/<int:pid>")
def delete_post(pid):
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "pid": pid,
    }
    
    data2 = {
        "post_id": pid,
    }
    like.Like.delete_post_likes(data2)
    comment.Comment.delete_post_comments(data2)
    post.Post.delete_post(data)
    return redirect("/dashboard")


@app.route("/edit/comment/<int:id>")
def edit_comment(id):
    if "user_id" not in session:
        return redirect("/logout")
    
    user_data = {
        "id" : session["user_id"]
    }
    
    
    data = {
        "id" : id
    }
    return render_template("updateComment.html", 
                            user = user.User.get_user(user_data), 
                            one_comment = comment.Comment.get_comment(data))
    
    

@app.route("/delete/comment/<int:id>/<int:pid>")
def delete_comment(id, pid):
    data = {
        "id": id,
        "post_id": pid
    }
    comment.Comment.delete_comment(data)
    return redirect(f"/view/post/{pid}")



@app.route("/add/comment", methods= ['POST'])
def add_comment():
    if "user_id" not in session:
        return redirect("/logout")
    
    if comment.Comment.is_valid(request.form):
        data = {
            "content" : request.form["content"],
            "user_id" : request.form["user_id"],
            "post_id" : request.form["post_id"]
        }
        comment.Comment.add_comment(data)
        return redirect(f"/view/post/{request.form['post_id']}")
    else:
        return redirect(f"/view/post/{request.form['post_id']}")
    

@app.route("/update/comment", methods= ['POST'])
def update_comment():
    if "user_id" not in session:
        return redirect("/logout")
    
    if comment.Comment.is_valid(request.form):
        data = {
            "id": request.form["id"],
            "content" : request.form["content"],
            "post_id": request.form["post_id"],
        }
        comment.Comment.update_comment(data)
        return redirect(f"/view/post/{request.form['post_id']}")
    else:
        return redirect(f"/edit/comment/{request.form['id']}")