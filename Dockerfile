# Use official Python image as base
FROM python:3.11-slim

# Set the working directory
# WORKDIR /app
WORKDIR /usr/src/app/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
