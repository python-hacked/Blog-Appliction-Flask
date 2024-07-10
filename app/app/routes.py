from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from . import db
from app.models import Blog, Category, Tag, User, Comment

api_bp = Blueprint('api', __name__, url_prefix='/api')
user_bp = Blueprint('user_api', __name__, url_prefix='/api/users')
tags_bp = Blueprint('tags', __name__, url_prefix='/api/tags')
comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

def geocode_address(address):
    # Replace with your Google Maps API key
    api_key = current_app.config.get('GOOGLE_MAPS_API_KEY')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

# User API

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists!'}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    if address:
        lat, lng = geocode_address(address)
    else:
        lat, lng = None, None

    new_user = User(username=username, email=email, password=hashed_password,
                    address=address, lat=lat, lng=lng)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize()), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.address = data.get('address', user.address)

    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='sha256')

    if 'address' in data:
        lat, lng = geocode_address(data['address'])
        user.lat = lat
        user.lng = lng

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@user_bp.route('/<int:user_id>/change-password', methods=['PUT'])
def change_password(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not check_password_hash(user.password, current_password):
        return jsonify({'error': 'Current password is incorrect!'}), 400

    user.password = generate_password_hash(new_password, method='sha256')

    db.session.commit()

    return jsonify({'message': 'Password changed successfully'}), 200

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Tag API

@tags_bp.route('', methods=['POST'])
def create_tag():
    data = request.json
    name = data.get('name')
    slug = data.get('slug')
    
    if not name or not slug:
        return jsonify({"error": "Name and slug are required"}), 400
    
    new_tag = Tag(name=name, slug=slug)
    db.session.add(new_tag)
    db.session.commit()
    
    return jsonify({
        "message": "Tag created successfully",
        "tag_id": new_tag.id
    }), 201

@tags_bp.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return jsonify({
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug
    })

@tags_bp.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    data = request.json
    
    tag.name = data.get('name', tag.name)
    tag.slug = data.get('slug', tag.slug)
    
    db.session.commit()
    
    return jsonify({
        "message": "Tag updated successfully"
    })

@tags_bp.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    
    return jsonify({
        "message": "Tag deleted successfully"
    })

# Comment API

@comments_bp.route('', methods=['POST'])
def create_comment():
    data = request.json
    content = data.get('content')
    user_id = data.get('user_id')
    blog_id = data.get('blog_id')
    
    if not content or not user_id or not blog_id:
        return jsonify({"error": "Content, user_id, and blog_id are required"}), 400
    
    new_comment = Comment(content=content, user_id=user_id, blog_id=blog_id)
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({
        "message": "Comment created successfully",
        "comment_id": new_comment.id
    }), 201

@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return jsonify({
        "id": comment.id,
        "content": comment.content,
        "creation_date": comment.creation_date.isoformat(),
        "user": {
            "id": comment.user.id,
            "username": comment.user.username
        },
        "blog": {
            "id": comment.blog.id,
            "title": comment.blog.title
        }
    })

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({
        "message": "Comment deleted successfully"
    })

# Blog API

@api_bp.route('/blogs', methods=['POST'])
def create_blog():
    data = request.json
    title = data.get('title')
    slug = data.get('slug')
    content = data.get('content')
    author_id = data.get('author_id')
    category_id = data.get('category_id')
    tags = data.get('tags', [])

    blog = Blog(title=title, slug=slug, content=content, author_id=author_id, category_id=category_id)

    for tag_id in tags:
        tag = Tag.query.get(tag_id)
        if tag:
            blog.tags.append(tag)

    db.session.add(blog)
    db.session.commit()

    return jsonify({'message': 'Blog created successfully', 'blog_id': blog.id}), 201

@api_bp.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return jsonify(blog.serialize()), 200

@api_bp.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    data = request.json

    blog.title = data.get('title', blog.title)
    blog.slug = data.get('slug', blog.slug)
    blog.content = data.get('content', blog.content)
    blog.category_id = data.get('category_id', blog.category_id)

    db.session.commit()

    return jsonify({'message': 'Blog updated successfully'}), 200

@api_bp.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return jsonify({'message': 'Blog deleted successfully'}), 200

# Category API

@api_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    name = data.get('name')
    slug = data.get('slug')

    category = Category(name=name, slug=slug)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully', 'category_id': category.id}), 201

@api_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.serialize()), 200

@api_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.json

    category.name = data.get('name', category.name)
    category.slug = data.get('slug', category.slug)

    db.session.commit()

    return jsonify({'message': 'Category updated successfully'}), 200

@api_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'Category deleted successfully'}), 200
