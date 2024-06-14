import requests
from flask import Flask, render_template
from post import Post

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


if __name__=="__main__":
    app.run(debug=True)