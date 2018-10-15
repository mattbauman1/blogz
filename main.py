from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from timestamp import Timestamp
from sortposts import SortPosts

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '12345'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    content = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime)

    def __init__(self, name, content, timestamp):
        self.name = name
        self.content = content
        self.timestamp = timestamp

    def __repr__(self):
        return repr((self.timestamp))

@app.route('/blog', methods=['GET'])
def blog():
    post_id = request.args.get('id')
    if post_id != None:
        post = Post.query.filter_by(id=post_id).all()
        timestamp = Timestamp(post[0].timestamp).timestampformatter()
        return render_template('blog.html', title=post[0].name, posts = post[0], timestamp = timestamp, individual_post = True)
    else:
        posts = Post.query.all()
        #for post in range(len(posts)):
            #posts[post].timestamp = Timestamp(posts[post].timestamp).totalstamp()
        #posts = SortPosts(posts).sortpostsbytimestampnormal()
        posts.sort(key=lambda post: post.timestamp, reverse=True)
        return render_template('blog.html', title="Build A Blog", posts = posts, individual_post = False)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        post_name = request.form.get('post_name')
        post_content = request.form.get('post_content')
        if post_name == "" or post_content == "" or len(post_name) > 60 or len(post_content) > 1000:
            title_error = ""
            content_error = ""
            if post_name == "":
                title_error = "Please fill in the title!"
            if post_content == "":
                content_error = "Please fill in the body!"
            if len(post_name) > 60:
                title_error = "Your title cannot be more than 60 characters."
            if len(post_content) > 1000:
                content_error = "Your body cannot be more than 1000 characters."
            return render_template('newpost.html', title="Add Blog Entry", title_error=title_error, content_error = content_error, old_name = post_name, old_post = post_content)
        new_post = Post(post_name, post_content, datetime.utcnow())
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog?id='+str(new_post.id))
    return render_template('newpost.html', title="Add Blog Entry")

if __name__ == '__main__':
    app.run()
