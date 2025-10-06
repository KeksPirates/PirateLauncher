from flask import Flask, jsonify
from data.scrapers.rutracker import scrape_rutracker, init
from data.models import SearchResponse

app = Flask(__name__)

debug = False
port = 8080

init()


@app.route('/search/<search_term>')
def search(search_term):
    try:
        response = scrape_rutracker(search_term)
        return jsonify(response.to_dict()), 200
    except RuntimeError as e:
        err = SearchResponse(success=False, query=search_term, data=[], count=0)
        return jsonify(err.to_dict()), 502


@app.route("/search/")
def search_empty():
    err = SearchResponse(success=False, query="", data=[], count=0)
    return jsonify(err.to_dict()), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)