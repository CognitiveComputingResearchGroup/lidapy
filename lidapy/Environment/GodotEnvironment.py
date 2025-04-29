#
# Godot AI Bridge (GAB) - Environment Action Client.
#
# Description: Used to submit movement and rotation actions to the agent in the
# DEMO environment
# Dependencies: PyZMQ (see https://pyzmq.readthedocs.io/en/latest/)
#

import json
import random
import time

import zmq  # Python Bindings for ZeroMq (PyZMQ)

from Environment.Environment import Environment
from Module.Initialization.DefaultLogger import getLogger
from MotorPlanExecution.MotorPlanExecutionImpl import \
    MotorPlanExecutionImpl

DEFAULT_TIMEOUT = 5000  # in milliseconds
DEFAULT_AGENT = 2
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 10002

# maps single character user inputs from command line to Godot agent actions
ACTION_MAP = {'W': 'up',
              'S': 'down',
              'A': 'left',
              'D': 'right',
              'Q': 'rotate_counterclockwise',
              'E': 'rotate_clockwise'}
verbose = False
seqno = 1  # current request's sequence number

class GodotEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.steps = 0
        self.done = False
        self.connection = None
        self.agent = DEFAULT_AGENT
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.col = 0
        self.row = 0
        self.position = {"row": self.row, "col": self.col}
        self.args = {"id": self.agent, "host": self.host, "port": self.port,
                     "verbose": verbose}
        self.state = {"done" : self.done}
        self.logger = getLogger(__class__.__name__).logger
        self.logger.debug("Initialized Godot Environment")

    def connect(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        """ Establishes a connection to Godot AI Bridge action listener.

        :param host: the GAB action listener's host IP address
        :param port: the GAB action listener's port number
        :return: socket connection
        """
        socket = zmq.Context().socket(zmq.REQ)
        socket.connect(f'tcp://{host}:{str(port)}')

        # without timeout the process can hang indefinitely
        socket.setsockopt(zmq.RCVTIMEO, DEFAULT_TIMEOUT)
        return socket

    def get_state(self):
        return self.state

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

    def notify(self, module):
        if isinstance(module, MotorPlanExecutionImpl):
            action = module.send_motor_plan()
            self.step(action)

    def reset(self):
        global seqno
        try:
            args = self.args
            if self.connection is None:
                self.connection = self.connect(host=args["host"],
                                               port=args["port"])

            # a global action counter (included in request payload)
            action_id = 0
            agent_id = args["id"]
            action = random.choice(list(ACTION_MAP.keys()))

            self.update_position(action)

            request = self.create_request(data={
                'event': {'type': 'action', 'agent': args["id"],
                          'value': ACTION_MAP[action]}})

            self.logger.debug(f"Row: {self.row}, Column: {self.col},"
                              f"Action: {ACTION_MAP[action]},"
                              f"Agent: {agent_id}")

            reply = self.send(self.connection, request)


            if args["verbose"]:
                print(f'\t REQUEST: {request}')
                print(f'\t REPLY: {reply}')

            self.steps += 1
            seqno += 1
            self.notify_observers()
        except Exception as e:
            print(e)

    def step(self, action):
        global seqno
        try:
            args = self.args
            if self.connection is None:
                self.connection = self.connect(host=args["host"],
                                               port=args["port"])

            # a global action counter (included in request payload)
            action_id = 0
            agent_id = args["id"]

            request = self.create_request(data={
                'event': {'type': 'action', 'agent': args["id"],
                          'value': ACTION_MAP[action]}})

            reply = self.send(self.connection, request)
            self.steps += 1
            self.update_position(action)
            self.logger.debug(f"Row: {self.row}, Column: {self.col},"
                              f"Action: {ACTION_MAP[action]},"
                              f"Agent: {agent_id}")

            if args["verbose"]:
                print(f'\t REQUEST: {request}')
                print(f'\t REPLY: {reply}')

            seqno += 1
            self.notify_observers()
        except Exception as e:
            print(e)

    def update_position(self, action):
        if action == 'W':  # up
            self.row = max(self.row - 1, 0)
        elif action == "D":  # Right
            self.col = self.col + 1
        elif action == 'S':  # down
            self.row = self.row + 1
        elif action == 'A':  # Left
            self.col = max(self.col - 1, 0)

    def get_position(self):
        return self.position

    def get_stimuli(self):
        return {"text" : ACTION_MAP}