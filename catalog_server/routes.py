from flask import request
from flask_app import app
from book import Book, topic_schema, item_schema, update_schema, dump_schema
from replication import replication, Replication
import cache

# Query-by-item request handler
def query_by_item(book_id):
    # Use the replication get method to make sure that the queried book is not outdated
    try:
        return replication.get(book_id)
    except (Replication.CouldNotGetUpdatedError, Replication.BookNotFoundError):
        return None


# Query-by-topic request handler
# The data returned by topic queries cannot be updated by end users
# so it doesn't need to be checked for different values at replicas
def query_by_topic(book_topic):
    # Use static method to get books by topic
    return Book.search(book_topic)

queries = {
    'by_item': {
        'handler': query_by_item,
        'schema': item_schema
    },
    'by_topic': {
        'handler': query_by_topic,
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
        book = Book.get(book_id)
    
    # If the book is None, that means that it doesn't exist in the database, so return an error message
    if book is None:
        return {'message': 'Not found'}, 404

    # Also, the order server will have the most up-to-date version of the book before modifying it
    # So the quantity updates should stay consistent across all servers

    # Use the replication method to update the book and make sure all other replicas get the updated book
    try:
        book = replication.update(book_id, book_data)

    # If the update failed, return a fail response
    except Replication.OutdatedError:
        return {'message': 'Update could not be processed because the item is not up to date'}, 409

    # Invalidate cache
    cache.invalidate_item(book_id)
    cache.invalidate_topic(book.topic)

    # book = Book.update(book_id,
    #                    # title=book_data.get('title'),
    #                    quantity=book_data.get('quantity'),
    #                    # topic=book_data.get('topic'),
    #                    price=book_data.get('price'))

    # Otherwise, return the updated information of the book formatted with the schema object
    return update_schema.jsonify(book)

# Dump endpoint
@app.route('/dump/', methods=['GET'])
def dump():
    return dump_schema.jsonify(Book.dump())

