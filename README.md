## Flask Blog Application API 
This repository contains a Flask-based API for managing a blog application. It provides endpoints for creating, reading, updating, and deleting blogs, categories, tags, users, and comments.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.x
pip (Python package installer)
Docker (optional, for Docker deployment)


git clone https://github.com/gitaleut/Satish_A1.git
cd app

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Example .env file
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask run

# With Docker
docker build -t app.
docker run -p 5000:5000 app

# Test Database 
python populate_data.py




