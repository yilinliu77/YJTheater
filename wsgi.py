import socketio

# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

if __name__ == "__main__":
    app.run(port=5001, host="127.0.0.1", threaded=True)