from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

DATA_PATH = '/home/ubuntu/Scrapper/Stock_Analyzer/structured_data/structured_company_data.json' 

@app.route('/api/data', methods=['GET'])

def get_data():
    # try:
    #     if os.path.exists(DATA_PATH):
    #         with open(DATA_PATH, 'r') as file:
    #             data = json.load(file)
    #         return jsonify(data)
    #     else:
    #         return jsonify({"error": "Data file not found"}), 404
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=800, debug=True)