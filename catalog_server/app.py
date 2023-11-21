from flask import Flask
from flask_app import app, port
from errorhandles import *  # Import error handlers directly
from routes import *  # Import routes directly
from database import create_database

# Create the Flask application instance
app = Flask(__name__)

# Import error handler overrides (assuming errorhandles.py contains the overrides)
import errorhandles

# Import routes (assuming routes.py contains the routes)
import routes

# Create the database file if it does not exist and add books to it
create_database()

# Run the Flask application instance
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
