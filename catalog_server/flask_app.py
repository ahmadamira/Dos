from flask import Flask
from os import environ

# Create a Flask application instance
app = Flask(__name__)

# Retrieve addresses of the front end and order servers from environment variables
ORDER_ADDRESS = environ.get('ORDER_ADDRESS')
FRONT_END_ADDRESS = environ.get('FRONT_END_ADDRESS')

# Configure Flask environment settings
app.config['FLASK_ENV'] = environ.get('FLASK_ENV', 'production')  # Default to 'production'
app.config['FLASK_DEBUG'] = bool(environ.get('FLASK_DEBUG', False))  # Default to False

# Get the application port from the environment variables, defaulting to 5000 if not set
port = int(environ.get('FLASK_PORT', 5000))

if __name__ == '__main__':
    # Run the Flask application instance
    app.run(host="0.0.0.0", port=port)
