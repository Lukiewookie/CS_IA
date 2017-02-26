#!/usr/bin/python
import psutil
import socket
import time


class DataGatherer:

    """Gathers the HW info"""

    def __init__(self):
        # Gathering information about CPU Usage
        self.cpu_usage = psutil.cpu_percent(1, False)  # (Time period, Multicore?)
        # Gathering info about SWAP usage
        self.ram_usage = psutil.virtual_memory()


class ConnectionSender:

    """Manages the connection to the server"""

    def __init__(self):

        sock = socket.socket()
        host = '127.0.0.1'
        port = 52000

        sock.connect((host, port))

        while True:
            time.sleep(1)
            sock.send("THIS IS A TEST")

ConnectionSender()

