# server.py
from flask import Flask, jsonify
from monsterscrap import scrape_website
import requests

app = Flask(__name__)


@app.route('/api/scrape', methods=['GET'])
def api_scrape():
    scraped_data = scrape_website('https://www.naukri.com/data-scientist-jobs-')
    
    if scraped_data:
        return jsonify(scraped_data)
    else:
        return jsonify({'error': 'Failed to scrape data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
