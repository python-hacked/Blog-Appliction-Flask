import os
from faker import Faker
from . import create_app, db
from app.models import User, Blog, Category, Tag, Comment
from werkzeug.security import generate_password_hash

fake = Faker()

def create_users(n):
    users = []
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=generate_password_hash("password", method='sha256'),
            address=fake.address(),
            lat=fake.latitude(),
            lng=fake.longitude()
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users

def create_categories(n):
    categories = []
    for _ in range(n):
        category = Category(
            name=fake.word(),
            slug=fake.slug()
        )
        categories.append(category)
        db.session.add(category)
    db.session.commit()
    return categories

def create_tags(n):
    tags = []
    for _ in range(n):
        tag = Tag(
            name=fake.word(),
            slug=fake.slug()
        )
        tags.append(tag)
        db.session.add(tag)
    db.session.commit()
    return tags

def create_blogs(users, categories, tags, n):
    blogs = []
    for _ in range(n):
        blog = Blog(
            title=fake.sentence(),
            slug=fake.slug(),
            content=fake.paragraph(),
            author_id=fake.random_element(users).id,
            category_id=fake.random_element(categories).id
        )
        # Randomly assign tags to the blog
        for tag in fake.random_elements(tags, length=fake.random_int(min=1, max=3)):
            blog.tags.append(tag)
        blogs.append(blog)
        db.session.add(blog)
    db.session.commit()
    return blogs

def create_comments(users, blogs, n):
    comments = []
    for _ in range(n):
        comment = Comment(
            content=fake.text(),
            user_id=fake.random_element(users).id,
            blog_id=fake.random_element(blogs).id
        )
        comments.append(comment)
        db.session.add(comment)
    db.session.commit()
    return comments

def populate_database():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        users = create_users(10)
        categories = create_categories(5)
        tags = create_tags(10)
        blogs = create_blogs(users, categories, tags, 20)
        comments = create_comments(users, blogs, 50)

        print("Database populated with test data.")

if __name__ == '__main__':
    populate_database()
