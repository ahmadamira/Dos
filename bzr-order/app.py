from flask import Flask
from flask_app import app, port




# Import error handler overrides (assuming errorhandles.py contains the overrides)
import errorhandles

# Import routes (assuming routes.py contains the routes)
import routes


# Run the Flask application instance
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
