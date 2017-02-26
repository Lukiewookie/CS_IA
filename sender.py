#!/usr/bin/python
import psutil
import socket
import time


class ConnectionSender:

    """Manages the connection to the server"""

    def __init__(self):

        sock = socket.socket()
        host = '127.0.0.1'
        port = 52000

        sock.connect((host, port))

        system_name = str(socket.gethostname())
        print system_name
        # sock.send(system_name)

        while True:
            ConnectionSender.data(self)
            time.sleep(0.1)
            sock.send(self.cpu_usage)
            time.sleep(0.1)
            sock.send(self.ram_usage)
            time.sleep(0.1)
            sock.send(self.disk_usage)
            time.sleep(0.1)
            sock.send(self.net_sent)
            time.sleep(0.1)
            sock.send(self.net_recv)

    def data(self):
        # Gathering CPU usage
        self.cpu_usage = str(psutil.cpu_percent(1, True))[1:-1]  # Time period, multicore
        # Gathering RAM usage
        self.ram_usage = str(psutil.virtual_memory().percent)  # Return type is tuple (wo/ str)
        # Gathering DISK usage
        self.disk_usage = str(psutil.disk_usage('/').used/1048576)
        # Gather amount of sent data
        self.net_sent = str(psutil.net_io_counters().bytes_sent/1000)
        # Gather amount of recv data
        self.net_recv = str(psutil.net_io_counters().bytes_recv/1000)


ConnectionSender()

