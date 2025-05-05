from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Define the path to your JSON file
DATA_PATH = '/path/to/your/json/file.json'  # Replace with your actual file path

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Check if file exists
        if os.path.exists(DATA_PATH):
            # Read JSON file
            with open(DATA_PATH, 'r') as file:
                data = json.load(file)
            return jsonify(data)
        else:
            return jsonify({"error": "Data file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to make it accessible from outside
    app.run(host='0.0.0.0', port=5000)