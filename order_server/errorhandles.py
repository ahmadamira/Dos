from flask_app import app

# Override the default error messages to JSON messages

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(e):
    return {'message': 'The requested URL was not found on the server. If you entered the URL manually, please check '
                       'your spelling and try again.'}, 404

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return {'message': 'The server encountered an internal error and was unable to complete your request. Either the '
                       'server is overloaded, or there is an error in the application.'}, 500

# Error handler for 405 Method Not Allowed
@app.errorhandler(405)
def method_not_allowed(e):
    return {'message': 'The method is not allowed for the requested URL.'}, 405
