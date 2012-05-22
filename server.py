#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
import zmq
import json

context = zmq.Context()

#  Socket to talk to clients
socket = context.socket(zmq.REPr)
socket.connect ("tcp://*:5555")

queue = []

while True
    message = socket.recv()
    queue.extend(json.loads(message))
    del(queue[0])
    socket.send(queue[0])
