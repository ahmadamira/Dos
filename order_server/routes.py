from flask_app import app
import requests

CATALOG_ADDRESSE = [
    "http://catalog_server_1:5000",
    "http://catalog_server_2:5007"
]


timeout = (0.15, 1.5)

@app.route('/buy/<book_id>', methods=['PUT'])
def buy(book_id):
    if not book_id.isnumeric():
        return {'message': 'Invalid book ID. Please provide a numeric ID.'}, 422

    while True:
        try:
            # Query the book from the catalog server
            book_response = requests.get(f'{CATALOG_ADDRESSE}/search/by_item/{book_id}')

        except requests.RequestException:
            return {'message': 'Could not connect to the catalog server'}, 504
        
        if book_response.status_code == 404:
            return {'message': 'Book not found.'}, 404
        
        elif book_response.status_code != 200:
            return book_response.content, book_response.status_code, book_response.headers.items()

        

        book = book_response.json()

        if book['quantity'] <= 0:
            return {'success': False, 'message': 'Book is out of stock.'}

        try:
            # Update the book quantity on the catalog server
            update_response = requests.put(f'{CATALOG_ADDRESSE}/modify/{book_id}', json={'quantity': book['quantity'] - 1})

        except requests.RequestException:
            return {'message': 'Could not connect to the catalog server'}, 504

        if update_response.status_code == 409:
            continue

        if update_response.status_code != 200:
            return update_response.text, update_response.status_code, update_response.headers.items()
        
        else:
            break

    return {'success': True, 'message': 'Book purchased successfully.'}
