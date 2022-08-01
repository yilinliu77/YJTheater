from flask import Flask, render_template, request

# import socketio
from flask_socketio import SocketIO

from json import *
import json



app = Flask(__name__)

sio = SocketIO(app)
# sio = socketio.Server(async_mode='gevent')
# sio = socketio.Server(async_mode='threading')
# sio = socketio.Server()

# app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

users = []
room = None

#type_list = {
#    "1":"开心",
#    "2":"伤心",
#    "3":"生气",
#    "0":"其他"
#}


class VideoNode:
  def __init__(self, name, showtime=9999, vtype="其他", holdername="",description = "", count = 0):
    self.name = name
    #self.id = vid
    self.showtime = showtime 
    self.vtype = vtype
    self.holdername =holdername 
    self.description = description
    self.votecount = count




video_list = [
    {"name":"CN.720P","source":"static/720p.mp4"},
    {"name":"SZU 2K","source":"http://172.31.178.220:8080/1080p.mp4"},
    {"name":"SZU 4K","source":"http://172.31.178.220:8080/2160p.mp4"},
    {"name":"PC Source (8000)","source":"http://127.0.0.1:8080/video.mp4"},
]

ip_list = [
    # "182.134.148.189",
    "127.0.0.1"
]

'''
Video List (For vote)
'''
video_list_global = [
    VideoNode("ququ's movie", count=10000),
    VideoNode("Sally"),
    VideoNode("Harry"),
    VideoNode("kkk")
]

video_queue_global = [
    VideoNode(
        "样例",
        showtime=33,
        vtype="其他",
        holdername="qq")
]



#video_queue_global = []

def VideoList2Dict(video_list):
    vote_list = {}
    show_num = min(4, len(video_list))
    for i in range(show_num): # not necessary to show total list
        vote_list[str(i)] = {
            "name": video_list[i].name,
            "videotype": video_list[i].vtype,
            "showtime": video_list[i].showtime,
            "holdername": video_list[i].holdername,
            "description": video_list[i].description
        }
    return vote_list

def Dict2VideoList(video_dict):
    vote_queue = []
    for id, data in video_dict.items():
        vote_queue.append(
            VideoNode(data['name'], 
            showtime=data['showtime'], 
            vtype=data['videotype'],
            holdername = data['holdername'],
            description = data['description'])
        )

    return vote_queue

def SaveQueue(vlist):
    f = open("queue.txt", "w+")
    d = VideoList2Dict(vlist)
    js = json.dumps(d)
    f.write(js)
    f.close()

def ReadQueue():
    f = open("queue.txt", "r")
    js = f.read()
    vlist = []
    #if js == NULL: return vlist
    d = json.loads(js)
    f.close()
    vlist = Dict2VideoList(d)
    return vlist



@app.route("/")
def index():
    # NOTE: ensure queue.txt is not empty before read
    video_queue_global = ReadQueue()
    print(video_queue_global[0])
    #input_votenum = SetupVideoList(video_list_global)
    input_video_queue = VideoList2Dict(video_queue_global)

    ip = request.remote_addr

    return render_template("index.html",
        sources=video_list, video_queue = input_video_queue)


@app.route("/test")
def test():
    return "test"


@app.route('/inqueue/', methods=['GET', 'POST'])
def register():
    print(request.form)     # 获取form表单提交过来的非文件数据,类似字典
    for item in request.form:
        print(item)

    data = request.form
    id = len(video_queue_global)
    name = str(data['videoname'])
    video_queue_global.append(
        VideoNode(name, 
        showtime=data['showtime'], 
        #vtype=type_list[data['videotype']],
        vtype=data['videotype'],
        holdername = data['holdername'],
        description = data['description']
        )
    ) # Make sure: id == index

    input_video_queue = VideoList2Dict(video_queue_global)
    SaveQueue(video_queue_global)
    #votenum[str(msg)]["count"] += 1
    sio.emit("display_queue", input_video_queue)
    return '注册成功'




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
    #video_list_global[int(str(msg))]["count"] += 1 # Make sure: id == index
    video_list_global[int(str(msg))].votecount += 1 # Make sure: id == index
    input_votenum = VideoList2Dict(video_list_global)
    #votenum[str(msg)]["count"] += 1
    sio.emit("display_vote", input_votenum)
    pass


@sio.on('popqueue')
def popqueue(msg):
    print(str(msg))

    video_queue_global.pop(0)
    # TODO: save queue
    SaveQueue(video_queue_global)

    input_video_queue = VideoList2Dict(video_queue_global)
    #votenum[str(msg)]["count"] += 1
    sio.emit("display_queue", input_video_queue)
    pass


if __name__ == "__main__":
    # app.run(threaded=True,port=5002)
    # app.run(host="0.0.0.0",port=5001, threaded=True)
    # app.run(host="0.0.0.0",port=5003, threaded=True)
    sio.run(app, host="0.0.0.0", port=5003)