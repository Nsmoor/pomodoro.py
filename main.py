# Import and setup logging
import logging
log_format = "[%(levelname)s] %(asctime)s [%(module)s:%(lineno)d] %(message)s"
logging.basicConfig(format=log_format, level=logging.DEBUG)

# Import classes
from pomodoro import Pomodoro
# Import the signal module to catch CTRL+C events
import signal

# Import the package for the web server
from flask import Flask

# Import the package SocketIO for the WebSocket
from flask_socketio import SocketIO


def handle_control_c(signal, frame):
    pomodoro.stop()
    exit()


#construct a pomodoro object
pomodoro = Pomodoro()
pomodoro.start()

# Create a webserver object called 'Shared Pomodoro' and keep track of it in the variable called server
server = Flask("Shared Pomodoro")
# Create a socketio object to handle web sockets

socketio = SocketIO(server, cors_allowed_origins="*")

signal.signal(signal.SIGINT, handle_control_c)


# Define a Websocket event 'json'
@socketio.on('json')
# Define the function 'handle_json_event()' with a parameter 'data' (dictionary) and connect it to the event 'json'
def handle_json_event(data):
    # Log all event data with he debug level 'debug'
    logging.debug('received message: ' + str(data))
    # if there is a key 'action' in the dictionary 'data'
    if "action" in data:
        # if the action is 'press'
        if data["action"] == "press":
            # call the method pressButton() of pomodoro
            pomodoro.press()


# Define an HTTP route / to serve the pomodoro page
@server.route('/')
# Define the function 'serve_index_page()' and connect it to the route /
def serve_index_page():
    # Return the static file 'index.html'
    return server.send_static_file('index.html')


# Start the webserver
socketio.run(server, host="0.0.0.0", debug=True)
