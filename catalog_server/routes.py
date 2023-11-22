from flask import request
from flask_app import app
from book import Book, topic_schema, item_schema, update_schema

def retrieve_item(book_id):
    return Book.retrieve_by_id(book_id)

def retrieve_by_topic(book_topic):
    return Book.retrieve_by_topic(book_topic)

queries = {
    'by_item': {
        'handler': retrieve_item,
        'schema': item_schema
    },
    'by_topic': {
        'handler': retrieve_by_topic,
        'schema': topic_schema
    }
}

@app.route('/', methods=['GET'])
def home():
    return "Greetings!"

@app.route('/search/<method>/<param>', methods=['GET'])
def query(method, param):
    if method not in queries:
        return {'message': 'Invalid search method', 'supportedMethods': list(queries.keys())}, 404

    result = queries[method]['handler'](param)

    if result is None:
        return {'message': 'Not found'}, 404

    return queries[method]['schema'].jsonify(result)

@app.route('/modify/<book_id>', methods=['PUT'])
def update(book_id):
    book_data = request.json

    if book_data is None:
        book_data = {}

    modified_book = Book.update(book_id,
                               title=book_data.get('title'),
                               quantity=book_data.get('quantity'),
                               topic=book_data.get('topic'),
                               price=book_data.get('price'))

    if modified_book is None:
        return {'message': 'Not found'}, 404

    return update_schema.jsonify(modified_book)
