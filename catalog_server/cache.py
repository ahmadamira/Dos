import requests
FRONT_END_ADDRESS = "http://flask_app_2:5003"


# Send a request to the front end server to invalidate a book
def invalidate_item(book_id):
    requests.delete(f'{FRONT_END_ADDRESS}/new/invalidate/item/{book_id}')


# Send a request to the front end server to invalidate a topic
# The topic data does not change, so this is not of any use right now
def invalidate_topic(book_topic):
    requests.delete(f'{FRONT_END_ADDRESS}/new/invalidate/topic/{book_topic}')