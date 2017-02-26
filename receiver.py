#!/usr/bin/python
import smtplib
import socket
from thread import *
import logging
import time
import threading


class ConnectionReceiver:

    """Gets data from each client by creating a thread for each of them"""

    def client_thread(self, connection_counter, conn):

        peer_name = str(connection_counter)


        threading.Thread(target=LoggerClass, args=peer_name).start()

        # infinite loop so that function do not terminate and thread do not end.
        while True:
            # Receiving from client
            data = conn.recv(1024)  # Receive 1024 bytes of data
            print data
            LoggerClass.cpu_log(peer_name, data)  # Log it to file

            time.sleep(0.5)  # wait for the other transmissions

            data = conn.recv(1024)
            print data
            LoggerClass.ram_log(peer_name, data)

            time.sleep(0.5)

    def __init__(self):
        # Variable definitions
        host = 'localhost'
        port = 52000

        connection_counter = 1

        sock = socket.socket()

        sock.bind((host, port))
        sock.listen(5)

        while True:
            conn, addr = sock.accept()  # Accepting incoming connections
            # Creating new thread. Calling client_thread function for this function and passing conn as argument.
            try:
                threading.Thread(target=ConnectionReceiver.client_thread, args=(self, connection_counter, conn)).start()
                connection_counter += 1
            except:
                pass


class LoggerClass:

    """Class that logs down the received data from each node"""

    def __init__(self, peer_name):
        # create the thread's logger
        logger = logging.getLogger('node-%s' % peer_name)
        logger.setLevel(logging.INFO)
        # create a file handler writing to a file named after the thread
        file_handler = logging.FileHandler('node-%s.log' % peer_name)
        # create a custom formatter and register it for the file handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        # register the file handler for the thread-specific logger
        logger.addHandler(file_handler)

    @staticmethod
    def cpu_log(peer_name, data):
        # Log CPU data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("CPU: %s", data)

    @staticmethod
    def ram_log(peer_name, data):
        # Log RAM data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("RAM: %s", data)


class AdminNotifier:

    """Notifies the admin of a change in the system"""

    def __init__(self):
        email_sender()

    def email_sender(self):
        # Simple email sending
        # Tutorial: http://naelshiab.com/tutorial-send-email-python/
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login("boinc@bsj.sch.id", "bertha2016")

        self.server.sendmail("boinc@bsj.sch.id", "17hejcmanl@bsj.sch.id", "One of the nodes has not reported back in an hour.")
        self.server.quit()

ConnectionReceiver()