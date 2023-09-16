import socketio
import typing
import asyncio

# connects to internal proxy and uses that as server

__socket = socketio.Client()

def open():
    __socket.connect('http://localhost:4041') # because we can't have Python 3.7 or higher
def close():
    __socket.disconnect()

def on(ev: str, cb: typing.Callable[[typing.Any], None]):
    @__socket.on(ev)
    def handle(data):
        cb(data)

def emit(ev: str, data):
    if __socket.connected:
        __socket.emit(ev, data)

@__socket.on('disconnect')
def __disconnect():
    print('----- SERVER DISCONNECTED')
@__socket.on('connect')
def __connect():
    print('----- SERVER CONNECTED')

@__socket.on('ping')
def __ping(n):
    __socket.emit('pong', n)