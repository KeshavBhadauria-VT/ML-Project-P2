from flask import Flask, jsonify
from nba_api.stats.static import players
import sys
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message='Hello, World!')

@app.route('/api/get_players', methods=['GET'])
def get_players():
    return jsonify(data=players.get_active_players())
    

if __name__ == '__main__':
    app.run(debug=True)