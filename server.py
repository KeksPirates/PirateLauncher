from flask import Flask, jsonify
from data.scrapers.rutracker import scrape_rutracker, init
from data.models import SearchResponse
import time

app = Flask(__name__)

debug = False
port = 8080
cache = {}

init()

@app.route('/search/<search_term>')
def search(search_term):
    current_time = time.time()
    
    expired_keys = [key for key, (response, timestamp) in cache.items() if current_time - timestamp >= 300]
    for key in expired_keys:
        del cache[key]
    
    if search_term in cache:
        response, timestamp = cache[search_term]
        return jsonify(response.to_dict()), 200
    
    try:
        response = scrape_rutracker(search_term)
        cache[search_term] = (response, current_time)
        return jsonify(response.to_dict()), 200
    except RuntimeError as e:
        err = SearchResponse(success=False, query=search_term, data=[], count=0)
        return jsonify(err.to_dict()), 502

@app.route("/search/")
def search_empty():
    err = SearchResponse(success=False, query="", data=[], count=0)
    return jsonify(err.to_dict()), 400

@app.route("/ping/")
def upping():
    return jsonify({"message": "pong"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)