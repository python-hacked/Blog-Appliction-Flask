from app import app

if __name__ == '__main__':
    print(app.url_map)  # Print all the routes in the application
    app.run(debug=True)
