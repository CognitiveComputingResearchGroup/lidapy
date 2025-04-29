import json
import time

import zmq  # Python Bindings for ZeroMq (PyZMQ)

DEFAULT_TIMEOUT = 5000  # in milliseconds

DEFAULT_AGENT = 1
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 10002

# maps single character user inputs from command line to Godot agent actions
ACTION_MAP = {'up' : 'W',
              'down' : 'S',
              'left' : 'A',
              'right' : 'D',
              'rotate_counterclockwise' : 'Q',
              'rotate_clockwise' : 'E'}
verbose = False
seqno = 1  # current request's sequence number

class Publisher:
    def __init__(self):
        self.context = zmq.Context()
        self.connection = self.connect()
        self.action_map = ACTION_MAP
        self.id = DEFAULT_AGENT

    def connect(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        """ Establishes a connection to Godot AI Bridge action listener.

            :param host: the GAB action listener's host IP address
            :param port: the GAB action listener's port number
            :return: socket connection
            """
        socket = self.context.socket(zmq.REQ)
        socket.connect(f'tcp://{host}:{str(port)}')

        # without timeout the process can hang indefinitely
        socket.setsockopt(zmq.RCVTIMEO, DEFAULT_TIMEOUT)
        return socket


    def send(self, connection, request):
        """ Encodes request and sends it to the GAB action listener.

            :param connection: connection: a connection to the GAB action listener
            :param request: a dictionary containing the action request payload
            :return: GAB action listener's (SUCCESS or ERROR) reply
            """
        encoded_request = json.dumps(request)
        connection.send_string(encoded_request)
        return connection.recv_json()

    def create_request(self, data):
        global seqno
        header = {
            'seqno': seqno,
            'time': round(time.time() * 1000)  # current time in milliseconds
        }

        return {'header': header, 'data': data}