import json
import zmq  # Python Bindings for ZeroMq (PyZMQ)

DEFAULT_TIMEOUT = 5000  # in milliseconds
DEFAULT_AGENT = 1
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 10001

# by default, receives all published messages (i.e., all topics accepted)
MSG_TOPIC_FILTER = ''

class Subscriber:
    def __init__(self):
        self.context = zmq.Context()
        self.connection = self.connect()
        self.state = None

    def connect(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        """ Establishes a connection to Godot AI Bridge state publisher.

        :param host: the GAB state publisher's host IP address
        :param port: the GAB state publisher's port number
        :return: socket connection
        """
        # creates a ZeroMQ subscriber socket
        socket = zmq.Context().socket(zmq.SUB)

        socket.setsockopt_string(zmq.SUBSCRIBE, MSG_TOPIC_FILTER)
        socket.setsockopt(zmq.RCVTIMEO, DEFAULT_TIMEOUT)

        socket.connect(f'tcp://{host}:{str(port)}')
        return socket

    def receive(self, connection):
        """ Receives and decodes next message from the GAB state publisher,
        waiting until TIMEOUT reached in none available.

        :param connection: a connection to the GAB state publisher
        :return: a tuple containing the received message's topic and payload
        """
        msg = connection.recv_string()

        # messages are received as strings of the form: "<TOPIC> <JSON>".
        # this splits the message string into TOPIC
        # and JSON-encoded payload
        ndx = msg.find('{')
        topic, encoded_payload = msg[0:ndx - 1], msg[ndx:]

        # unmarshal JSON message content
        payload = json.loads(encoded_payload)

        return topic, payload