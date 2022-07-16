from flask import Flask, render_template, request

# import socketio
from flask_socketio import SocketIO

from json import *



app = Flask(__name__)

sio = SocketIO(app)
# sio = socketio.Server(async_mode='gevent')
# sio = socketio.Server(async_mode='threading')
# sio = socketio.Server()

# app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

users = []
room = None

video_list = [
    {"name":"CN.720P","source":"static/720p.mp4"},
    {"name":"SZU 2K","source":"http://172.31.178.220:8080/1080p.mp4"},
    {"name":"SZU 4K","source":"http://172.31.178.220:8080/2160p.mp4"},
    {"name":"PC Source (8000)","source":"http://127.0.0.1:8080/video.mp4"},
]

votenum = {
    "0": {
        "name": "致所有我曾爱过的男孩2",
        "count": 0
    },
    "1": {
        "name": "巴黎我爱你",
        "count": 0
    },
    "2": {
        "name": "Exit",
        "count": 0
    },
    "3": {
        "name": "null",
        "count": 0
    }
}

ip_list = [
    # "182.134.148.189",
    "127.0.0.1"
]


@app.route("/")
def index():
    ip = request.remote_addr
    return render_template("index.html",
        sources=video_list, votenum=votenum)


@app.route("/test")
def test():
    return "test"

@sio.on('register')
def register( msg):
    users.append({"nickname": msg["nickname"], "time": 0})
    sio.emit("registerUsers", dumps(users), broadcast=True, include_self=True)


@sio.on('timeReport')
def timeReport( msg):
    sio.emit("timeReport", {
             "time": msg["time"], "nickname": msg["nickname"]}, broadcast=True, include_self=True)


@sio.on('synchronize')
def synchronize(msg):
    sio.emit("synchronizeYourself", {
             "time": msg["time"], "nickname": msg["nickname"]}, broadcast=True, include_self=False)


@sio.on('play')
def play(msg):
    sio.emit("play", {"nickname": msg["nickname"]}, broadcast=True, include_self=False)


@sio.on('pause')
def pause(msg):
    sio.emit("pause", {"nickname": msg["nickname"]}, broadcast=True, include_self=False)


@sio.on('vote')
def vote(msg):
    votenum[str(msg)]["count"] += 1
    sio.emit("display_vote", votenum)
    pass


if __name__ == "__main__":
    # app.run(threaded=True,port=5002)
    # app.run(host="0.0.0.0",port=5001, threaded=True)
    # app.run(host="0.0.0.0",port=5003, threaded=True)
    sio.run(app, host="0.0.0.0", port=5003)