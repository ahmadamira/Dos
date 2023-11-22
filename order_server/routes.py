from flask_app import app
import requests

CATALOG_ADDRESS = "http://127.0.0.1:5000"

@app.route('/buy/<book_id>', methods=['PUT'])
def buy(book_id):
    if not book_id.isnumeric():
        return {'message': 'Invalid book ID. Please provide a numeric ID.'}, 422

    # Query the book from the catalog server
    book_response = requests.get(f'{CATALOG_ADDRESS}/search/by_item/{book_id}')

    if book_response.status_code == 404:
        return {'message': 'Book not found.'}, 404
    elif book_response.status_code != 200:
        return {'message': 'Error querying the catalog server.'}, 500

    book = book_response.json()

    if book['quantity'] <= 0:
        return {'success': False, 'message': 'Book is out of stock.'}

    # Update the book quantity on the catalog server
    update_response = requests.put(f'{CATALOG_ADDRESS}/modify/{book_id}', json={'quantity': book['quantity'] - 1})

    if update_response.status_code != 200:
        return {'message': 'Error updating the catalog server.'}, 500

    return {'success': True, 'message': 'Book purchased successfully.'}

