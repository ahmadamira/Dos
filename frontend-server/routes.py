from flask_app import app
from replication import custom_replication, custom_timeout
from cache import new_lookup_cache, new_search_cache, SearchEntry
from flask import jsonify
import requests

# Search endpoint
@app.route('/search/<book_topic>', methods=['GET'])
def search(book_topic):

     # If topic is in cache, just get the books from it
    if book_topic.lower() in new_search_cache:
        return jsonify(new_search_cache.get(book_topic.lower()).search_result)

    # Times to try to connect to catalog servers
    tries = custom_replication.get_catalog_count()

    for request_try in range(tries):
        try:
            # Get book from the catalog server
            response = requests.get(f'{custom_replication.get_catalog_address()}/query/topic/{book_topic}', timeout=custom_timeout)
            break
        except requests.RequestException:
            pass

    # If the loop completes all tries without being able to reach a server
    else:
        return {'message': 'Could not connect to a server to search'}, 504

    # If any books were found, cache their topics
    # This will cache all the topics found if the cache can fit
    if response.status_code == 200 and isinstance(response.json(), list):

        # Cache this search operation
        new_search_cache.insert(
            book_topic.lower(),
            SearchEntry(response.json())
        )

    # Return the catalog server response as-is
    return response.text, response.status_code, response.headers.items()


# Lookup endpoint
@app.route('/lookup/<book_id>', methods=['GET'])
def lookup(book_id):
    # If the ID is not a number, reject the lookup
    if not book_id.isnumeric():
        return {'message': 'Book ID must be a number'}, 422

        # If book is in cache, just get the book from it
    cached_book = new_lookup_cache.get(int(book_id))
    if cached_book is not None:
        return cached_book

    # Times to try to connect to catalog servers
    tries = custom_replication.get_catalog_count()

    for request_try in range(tries):
        try:
            # Get the list of books from the catalog server
            response = requests.get(f'{custom_replication.get_catalog_address()}/query/item/{book_id}', timeout=custom_timeout)
            break
        except requests.RequestException:
            pass
    # If the loop completes all tries without being able to reach a server
    else:
        return {'message': 'Could not connect to a server to search'}, 504

    # If the response status is 404 not found, override the error message
    if response.status_code == 404:
        return {'message': 'Book with the specified ID does not exist'}, 404
    
    # If response is OK, cache the obtained book
    elif response.status_code == 200:
        new_lookup_cache.insert(int(book_id), response.json())

    # Otherwise, return the catalog server response as-is
    return response.text, response.status_code, response.headers.items()


# Buy endpoint
@app.route('/buy/<book_id>', methods=['PUT'])
def buy(book_id):
    # If the ID is not a number, reject the purchase request
    if not book_id.isnumeric():
        return {'message': 'Book ID must be a number'}, 422

     # Times to try to connect to order servers
    tries = custom_replication.get_order_count()

    for request_try in range(tries):
        try:
            # Forward the request to the order server
            response = requests.put(f'{custom_replication.get_order_address()}/buy/{book_id}',
                                    timeout=tuple([_*2 for _ in custom_timeout]))
            if response.status_code == 504:
                continue
            break
        except requests.RequestException:
            pass
    # If the loop completes all tries without being able to reach a server
    else:
        return {'message': 'Could not connect to a server to lookup'}, 504

    # Return the response from the order server as-is
    return response.text, response.status_code, response.headers.items()
