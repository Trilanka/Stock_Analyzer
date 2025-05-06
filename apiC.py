from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

DATA_PATH = '/home/ubuntu/Scrapper/Stock_Analyzer/structured_data/structured_company_data.json' 

@app.route('/api/data', methods=['GET'])

def get_data():
    
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)