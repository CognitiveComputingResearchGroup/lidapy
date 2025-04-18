#
# Godot AI Bridge (GAB) - DEMO Environment Action Client.
#
# Description: Used to submit movement and rotation actions to the agent in the DEMO environment via CLI
# Dependencies: PyZMQ (see https://pyzmq.readthedocs.io/en/latest/)
#

import json
import argparse
import sys
import os
import time

import zmq  # Python Bindings for ZeroMq (PyZMQ)

DEFAULT_TIMEOUT = 5000  # in milliseconds

DEFAULT_AGENT = 1
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


def parse_args():
    """ Parses command line arguments.

    :return: argparse parser with parsed command line args
    """
    parser = argparse.ArgumentParser(description='Godot AI Bridge (GAB) - DEMO Environment Action Client')

    parser.add_argument('--id', type=int, required=False, default=DEFAULT_AGENT,
                        help=f'the id of the agent to which this action will be sent (default: {DEFAULT_AGENT})')
    parser.add_argument('--host', type=str, required=False, default=DEFAULT_HOST,
                        help=f'the IP address of host running the GAB action listener (default: {DEFAULT_HOST})')
    parser.add_argument('--port', type=int, required=False, default=DEFAULT_PORT,
                        help=f'the port number of the GAB action listener (default: {DEFAULT_PORT})')
    parser.add_argument('--verbose', required=False, action="store_true",
                        help='increases verbosity (displays requests & replies)')

    return parser.parse_args()


def connect(host=DEFAULT_HOST, port=DEFAULT_PORT):
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


def send(connection, request):
    """ Encodes request and sends it to the GAB action listener.

    :param connection: connection: a connection to the GAB action listener
    :param request: a dictionary containing the action request payload
    :return: GAB action listener's (SUCCESS or ERROR) reply
    """
    encoded_request = json.dumps(request)
    connection.send_string(encoded_request)
    return connection.recv_json()


def create_request(data):
    global seqno
    header = {
        'seqno': seqno,
        'time': round(time.time() * 1000)  # current time in milliseconds
    }

    return {'header': header, 'data': data}

def main():
    global seqno
    try:
        args = parse_args()
        connection = connect(host=args.host, port=args.port)

        # a global action counter (included in request payload)
        action_id = 0
        agent_id = args.id

        # MAIN LOOP: receive action via CLI, and send it to GAB action listener
        print('Select an action ID followed by [ENTER]. (All others quit.)')
        while True:
            action = input('>> A, W, S, D, Q, or E?  ').upper()
            if action not in ACTION_MAP:
                break

            request = create_request(data={'event':{'type':'action', 'agent': args.id, 'value':ACTION_MAP[action]}})
            reply = send(connection, request)

            if args.verbose:
                print(f'\t REQUEST: {request}')
                print(f'\t REPLY: {reply}')

            seqno += 1

    except KeyboardInterrupt:

        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)

if __name__ == '__main__':
    main()