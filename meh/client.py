#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
import zmq

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:5555")

for request in range (1,10):
    print "Sending request ", request,"…"
    socket.send ("Hello")
    
    #  Get the reply.
    message = socket.recv()
    print "Received reply ", request, "[", message, "]"
