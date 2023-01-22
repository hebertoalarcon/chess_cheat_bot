from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins":"*"}})
cors

socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)

@app.route("/game_moves", methods=['POST'])
def get_game_moves():

    data = request.json
    print(data)


    return jsonify(dict(message='ok')), 200


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")