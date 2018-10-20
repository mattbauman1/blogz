from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime
from timestamp import Timestamp

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '12345'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    content = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, content, timestamp, owner):
        self.name = name
        self.content = content
        self.timestamp = timestamp
        self.deleted = False
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(30))
    posts = db.relationship('Post', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

def username_verification(username):
    if username == "":
        return '"Username" cannot be blank!'
    elif re.match("^\s.", username) != None:
        return "You cannot have a space at the beginning of your username!"
    elif re.match("^.+\s+.", username) != None:
        return "You cannot have a space anywhere in your username!"
    elif re.match("^.+\s", username) != None:
        return "You cannot have a space at the end of your username!"
    elif re.match("^\^", username) or re.match("^.+\^", username) != None:
        return 'You cannot have a "^" in your username!'
    elif re.match("^[a-zA-Z0-9-_.]{3,20}$", username) == None:
        return 'The "Username" must be between 3 and 20 characters in length and can have no special characters or spaces.'
    else:
        return ""

def password_verification(password):
    if password == "":
        return '"Password" cannot be blank!'
    elif re.match("^[a-zA-Z0-9-_.]{3,20}$", password) == None:
        return 'The "Password" must be between 3 and 20 characters in length and can have no special characters or spaces'
    else:
        return ""

def verifypassword_verification(password, verifypassword):
    if verifypassword == "":
        return 'You must retype your "Password" here!'
    elif password != verifypassword:
        return "The passwords you entered do not match, please try again!"
    else:
        return ""

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'signup', 'index', 'logout']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/blog')

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    users.sort(key=lambda user: user.username)
    return render_template('index.html', title="Blogz", users = users)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if  request.method == 'POST':
        username = request.form.get('username')
        existing_user = User.query.filter_by(username=username).first()
        password = request.form.get('password')
        verifypassword = request.form.get('verifypassword')
        adjustable_username_error = username_verification(username)
        adjustable_password_error = password_verification(password)
        adjustable_verifypassword_error = verifypassword_verification(password, verifypassword)
        if existing_user and (adjustable_password_error != "" or adjustable_verifypassword_error != ""):
            return render_template('signup.html', title = "Blogz", username_error = 'The username "' + username + '" already exist, please choose a different username!', password_error = adjustable_password_error, verifypassword_error = adjustable_verifypassword_error)
        if adjustable_username_error != "" or adjustable_password_error != "" or adjustable_verifypassword_error != "":
            return render_template('signup.html', title = "Blogz", old_username_value = username, username_error = adjustable_username_error, password_error = adjustable_password_error, verifypassword_error = adjustable_verifypassword_error)
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/newpost')
    return render_template('signup.html', title = "Blogz")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            if not user:
                return render_template('login.html', title = "Blogz", old_username = username, username_error = True)
            else:
                return render_template('login.html', title = "Blogz", old_username = username, password_error = 'You entered an incorrect password for this account, please try again!')
    return render_template('login.html', title = "Blogz")

@app.route('/blog', methods=['GET'])
def blog():
    user_id = request.args.get('user')
    if user_id != None:
        owner = User.query.filter_by(id = user_id).first()
        posts = Post.query.filter_by(owner=owner).all()
        posts.sort(key=lambda post: post.timestamp, reverse=True)
        timestamps = []
        for post in range(len(posts)):
            timestamps.append(Timestamp(posts[post].timestamp).timestampformatter())
        return render_template('blog.html', title="Blogz", heading = owner.username + "'s Posts", posts = posts, timestamps = timestamps, individual_post = False)
    post_id = request.args.get('id')
    if post_id != None:
        post = Post.query.filter_by(id=post_id)
        timestamp = Timestamp(post[0].timestamp).timestampformatter()
        return render_template('blog.html', title=post[0].name, posts = post[0], timestamp = timestamp, individual_post = True)
    posts = Post.query.all()
    posts.sort(key=lambda post: post.timestamp, reverse=True)
    timestamps = []
    for post in range(len(posts)):
        timestamps.append(Timestamp(posts[post].timestamp).timestampformatter())
    return render_template('blog.html', title="Blogz", heading = "Blogz", posts = posts, timestamps = timestamps, individual_post = False)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        post_name = request.form.get('post_name')
        post_content = request.form.get('post_content')
        owner = User.query.filter_by(username = session['username']).first()
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
        new_post = Post(post_name, post_content, datetime.utcnow(), owner)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog?id='+str(new_post.id))
    return render_template('newpost.html', title="Add Blog Entry")

if __name__ == '__main__':
    app.run()
