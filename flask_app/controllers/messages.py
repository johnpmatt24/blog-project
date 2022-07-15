from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import message, user



@app.route("/user/message/<int:id>")
def message_Portal(id):
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "sender_id" : session["user_id"],
        "receiver_id" : id,
        
    }
    
    data2 = {
        "id" : id,
    }
    
    
    return render_template("messagePortal.html", 
                            user = user.User.get_user(data2),  
                            messages = message.Message.get_user_messages(data))



@app.route('/send/message', methods = ["POST"])
def send_message():
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "sender_id": request.form["sender_id"],   #sender_id and receiver_id will be hidden inputs
        "receiver_id": request.form['receiver_id'],
        "content" : request.form['content']
    }
    message.Message.save(data)
    return redirect(f"/user/message/{request.form['receiver_id']}")



@app.route("/delete/message/<int:mid>")
def delete_message(mid):
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "mid" : mid
    }
    
    message.Message.delete(data)
    return redirect("/messagePortal")



