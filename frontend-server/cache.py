from flask_app import app

# Define a new Cache class
class CustomCache:
    def __init__(self, max_size: int = 3):
        self.cache = {}
        self.lru_queue = []
        self.max_size = max_size

    def insert(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
            self.lru_queue.remove(key)

        if len(self.cache) >= self.max_size:
            remove_key = self.lru_queue.pop(0)
            self.cache.pop(remove_key)

        self.cache[key] = value
        self.lru_queue.append(key)

    def get(self, key):
        if key not in self.cache:
            return None

        self.lru_queue.remove(key)
        self.lru_queue.append(key)

        return self.cache[key]

    def remove(self, key):
        if key in self.cache:
            self.cache.pop(key)
            self.lru_queue.remove(key)

    def clear(self):
        self.cache.clear()
        self.lru_queue.clear()

    def ids(self):
        return list(self.lru_queue)

    def __contains__(self, key):
        return key in self.cache

# Define class for search entry
class SearchEntry:
    def __init__(self, search_result):
        # Set of topics stored in this entry
        # This is needed to invalidate the topic 
        self.topics = set([book['topic'] for book in search_result])

        # The entry itself
        self.search_result = search_result

    def __contains__(self, item):
        return item in self.topics

# Create instances of the new cache class
new_lookup_cache = CustomCache()
new_search_cache = CustomCache(max_size=10)

# Use the cache instances in your routes
@app.route('/new/invalidate/item/<item_id>', methods=['DELETE'])
def new_invalidate_item(item_id):
    new_lookup_cache.remove(int(item_id))
    return '', 204

@app.route('/new/invalidate/topic/', methods=['DELETE'])
def new_invalidate_all_topics():
    new_search_cache.clear()
    return '', 204

@app.route('/new/invalidate/topic/<topic>', methods=['DELETE'])
def new_invalidate_topic(topic):
    containing_entries = [key for key, value in new_search_cache.cache.items()
                          if topic in value.topics]

    for entry in containing_entries:
        new_search_cache.remove(entry)

    return '', 204

@app.route('/new/dump/', methods=['GET'])
def new_dump():
    response = {
        'lookup': [{'id': id, **new_lookup_cache.cache[id]} for id in new_lookup_cache.lru_queue],
        'search': [{'id': id,
                    'topics': list(new_search_cache.cache[id].topics),
                    'search_result': new_search_cache.cache[id].search_result}
                   for id in new_search_cache.lru_queue]
    }
    print(response)
    return response