from flask import Flask
from flask import jsonify
from scraping.rutracker import scrape_rutracker
from scraping.rutracker import init

app = Flask(__name__)



debug = False
port = 8080

init()


@app.route('/search/<search_term>')
def search(search_term):
    results = scrape_rutracker(search_term)
    if results is None:
        return jsonify(error="No results found"), 404
    return jsonify(results)

@app.route("/search/")
def search_empty():
    return jsonify(error="no search query defined"), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
