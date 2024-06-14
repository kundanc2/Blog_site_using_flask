import requests
from flask import Flask, render_template,request
from post import Post
import smtplib



OWN_EMAIL = "YOUR OWN EMAIL ADDRESS"
OWN_PASSWORD = "YOUR EMAIL ADDRESS PASSWORD"

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


post_objects=[]

posts =requests.get("https://api.npoint.io/cec3f87575a5af5bca03").json()
for post in posts:
    post_obj=Post(post["id"],post["title"],post["subtitle"],post["body"], post["image_url"])
    post_objects.append(post_obj)

app=Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html",post=posts)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

@app.route("/post/<int:blog_id>")
def post(blog_id):
    for post in post_objects:
        if post.id==blog_id:
            return render_template("post.html",post=post)

@app.route("/form-entry",methods=["POST","GET"])
def contact_form():
    if request.method == "POST":
        
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
        return render_template("contact.html",success=1)
    return render_template("contact.html",success=0)
if __name__=="__main__":
    app.run(debug=True)