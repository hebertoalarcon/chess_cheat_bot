from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from queue import Queue
from move_receiver import MoveReiceiver

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":"*"}})

socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)

work_queue = Queue()
move_receiver = MoveReiceiver(work_queue, socketio)

@app.before_first_request
def before_first_request():
    move_receiver.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game_moves", methods=["POST"])
def get_game_moves():

    data = request.json
    print(data)
    
    move_receiver.work_queue.put(data)

    socketio.emit('moves', data)

    return jsonify(dict(message='ok')), 200


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")