from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref=db.backref('blogs', lazy=True))
    category = db.relationship('Category', backref=db.backref('blogs', lazy=True))
    tags = db.relationship('Tag', secondary='blog_tags', lazy='subquery', backref=db.backref('blogs', lazy=True))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True, nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    blog = db.relationship('Blog', backref=db.backref('comments', lazy=True))

blog_tags = db.Table('blog_tags',
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)
