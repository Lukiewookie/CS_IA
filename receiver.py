#!/usr/bin/python
import smtplib
import socket
from thread import *
import logging


class ConnectionReceiver:

    """Gets data from each client by creating a thread for each of them"""

    @staticmethod
    def client_thread(connection_counter, conn):

        peer_name = connection_counter
        connection_counter -= 1

        LoggerClass(peer_name)

        # infinite loop so that function do not terminate and thread do not end.
        while True:
            # Receiving from client
            data = conn.recv(1024)  # Receive 1024 bytes of data
            print data

            LoggerClass.log(data)

    def __init__(self):
        # Keeps a track of how many connections took place
        connection_counter = 1
        # Variable definitions
        host = 'localhost'
        port = 52000

        sock = socket.socket()

        sock.bind((host, port))
        sock.listen(5)

        while True:
            conn, addr = sock.accept()  # Accepting incoming connections
            # Creating new thread. Calling client_thread function for this function and passing conn as argument.
            start_new_thread(ConnectionReceiver.client_thread(connection_counter, conn))  # start new thread
            # takes 1st argument as a function name to be run, second is the tuple of arguments to the function.


class LoggerClass:

    """Class that logs down the received data from each node"""

    def __init__(self, peer_name):

        logging.basicConfig(level=logging.INFO,
                            format='%(relativeCreated)6d %(threadName)s %(message)s',
                            filename='node-%s.log' % peer_name)

    @staticmethod
    def log(data):

        logging.info(data)


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