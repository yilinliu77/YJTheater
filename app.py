from flask import Flask, render_template, request
import socketio
from json import *

sio = socketio.Server(async_mode='threading')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

users = []
room = None

video_list = [
    {"name":"CN.1080P","source":"static/1080p.mp4"},
    {"name":"Local Source (8000)","source":"http://127.0.0.1:8080/1080p.mp4"},
    # {"name":"CN.720P","source":"static/720p.mp4"},
    # {"name":"CN.480P","source":"static/480p.mp4"},
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
def register(sid, msg):
    users.append({"nickname": msg["nickname"], "time": 0})
    sio.emit("registerUsers", dumps(users))


@sio.on('timeReport')
def timeReport(sid, msg):
    sio.emit("timeReport", {
             "time": msg["time"], "nickname": msg["nickname"]})


@sio.on('synchronize')
def synchronize(sid, msg):
    sio.emit("synchronizeYourself", {
             "time": msg["time"], "nickname": msg["nickname"]})


@sio.on('play')
def play(sid, msg):
    sio.emit("play", {"nickname": msg["nickname"]})


@sio.on('pause')
def pause(sid, msg):
    sio.emit("pause", {"nickname": msg["nickname"]})


@sio.on('vote')
def vote(sid, msg):
    votenum[str(msg)]["count"] += 1
    sio.emit("display_vote", votenum)
    pass


if __name__ == "__main__":

    # app.run(threaded=True)
    app.run(host="0.0.0.0", port=5001, threaded=True)
