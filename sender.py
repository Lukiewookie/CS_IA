#!/usr/bin/python
import psutil
import socket
import time
import logging
import platform


class ConnectionSender:

    """Manages the connection to the server"""

    def __init__(self):

        # Get the node name to make log writing simpler
        peer_name = socket.gethostname()
        print platform.system()

        '''
        For testing purposes, peer_name has been redefined below!!!
        '''
        # Delete this variable definition after testing phase
        peer_name = "LOCAL"

        Logger()

        sock = socket.socket()
        host = '127.0.0.1'
        port = 52000

        sock.connect((host, port))

        system_name = str(socket.gethostname())
        print system_name
        sock.send(system_name)

        sleeptime = 0.1

        while True:
            ConnectionSender.data(self)

            time.sleep(sleeptime)

            sock.send(self.cpu_usage)
            Logger.cpu_log(peer_name, self.cpu_usage)

            time.sleep(sleeptime)

            sock.send(self.ram_usage)
            Logger.ram_log(peer_name, self.ram_usage)

            time.sleep(sleeptime)

            sock.send(self.disk_usage)
            Logger.disk_log(peer_name, self.disk_usage)

            time.sleep(sleeptime)

            sock.send(self.net_sent)
            Logger.netsent_log(peer_name, self.net_sent)

            time.sleep(sleeptime)
            sock.send(self.net_recv)

            Logger.netrecv_log(peer_name, self.net_recv)

            Logger.spacer(peer_name)

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


class Logger:

    def __init__(self):

        peer_name = "LOCAL"

        # create the thread's logger
        logger = logging.getLogger('node-%s' % peer_name)
        logger.setLevel(logging.INFO)
        # create a file handler writing to a file named after the thread
        file_handler = logging.FileHandler('node-%s.log' % peer_name)
        # create a custom formatter and register it for the file handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')  # - %(levelname)s
        file_handler.setFormatter(formatter)
        # register the file handler for the thread-specific logger
        logger.addHandler(file_handler)

    @staticmethod
    def cpu_log(peer_name, data):
        # Log CPU data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("CPU Used: %s percent" % data)

    @staticmethod
    def ram_log(peer_name, data):
        # Log RAM data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("RAM Used: %s percent", data)

    @staticmethod
    def disk_log(peer_name, data):
        # Log DISK data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("DISK Used: %s MB", data)

    @staticmethod
    def netsent_log(peer_name, data):
        # Log Network SENT data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("KB Sent: %s", data)

    @staticmethod
    def netrecv_log(peer_name, data):
        # Log Network RECV data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("KB Received: %s", data)

    @staticmethod
    def spacer(peer_name):
        # Log Network RECV data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info(' ')

    @staticmethod
    def spacer(peer_name):
        # Log Network RECV data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info(' ')


ConnectionSender()
