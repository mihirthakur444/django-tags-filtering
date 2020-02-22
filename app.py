from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------------------------------------------------------------------------
# MODELS
blog_tag = db.Table('post_tag',
db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text(500))
    tags = db.relationship('Tag',secondary=blog_tag, back_populates="name")
    # timestamp = db.Column(db.DateTime)
    # uuid = db.Column(db.String(255))
    def __init__(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags = tags

    def __repr__(self):
        return "Title: {}".format(self.title)

class Tag(db.Model):
    """SQLAlchemy Tag object class"""
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    posts = db.relationship('Post', secondary = blog_tag,
                            back_populates = "tags")
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Title: {}".format(self.name)

# ---------------------------------------------------------------------------------
# ROUTES
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    """Take the list of tags and turn them into an array"""
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        # post.uuid = uid.hex
        tag_string = request.form['tags'] #post_form.tags.data
        tags = tag_string.split(",")
        for tag in tags:
            post_tag = add_tags(tag)
            print(post_tag)
            post.tags.append(post_tag)
        new_post = Post(title=post_title, content=post_content, author=post_author, tags=post_tag)
        db.session.add(post)
        db.session.commit()
        return redirect('/posts')
        # flash (u'New Post Created!', 'alert-info')
    else:
        all_posts = Post.query.order_by().all()
    return render_template('posts.html', posts=all_posts)

@app.route('/')
def index():
    return render_template('home.html')
# ---------------------------------------------------------------------------------

def add_tags(tag):
    existing_tag = Tag.query.filter(Tag.name == tag.lower()).one_or_none()
    """if it does return existing tag objec to list"""
    if existing_tag is not None:
        return existing_tag
    else:
       new_tag = Tag()
       new_tag.name = tag.lower()
       return new_tag
