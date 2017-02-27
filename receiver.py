#!/usr/bin/python
import smtplib
import socket
import logging
import time
import threading

from distutils.dir_util import copy_tree

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


class ConnectionReceiver:

    """Gets data from each client by creating a thread for each of them"""

    def client_thread(self, connection_counter, conn):

        peer_name = str(connection_counter)

        """
        Y U NO WORK
        peer_name = str(conn.recv(100))
        print peer_name
        print type(peer_name)
        """

        threading.Thread(target=LoggerClass, args=peer_name).start()
        # Sets the amount of time between the different connection. Change this to change the frequency of logging
        sleeptime = 0.1
        # infinite loop so that function do not terminate and thread do not end.
        while True:

            try:  # Error handling
                # Receiving from client
                data = conn.recv(1024)  # Receive 1024 bytes of data
                print data
                LoggerClass.cpu_log(peer_name, data)  # Log it to file

                time.sleep(sleeptime)  # wait for the other transmissions

                data = conn.recv(1024)
                print data
                LoggerClass.ram_log(peer_name, data)

                time.sleep(sleeptime)

                data = conn.recv(1024)
                print data
                LoggerClass.disk_log(peer_name, data)

                time.sleep(sleeptime)

                data = conn.recv(1024)
                print data
                LoggerClass.netsent_log(peer_name, data)

                time.sleep(sleeptime)

                data = conn.recv(1024)
                print data
                LoggerClass.netrecv_log(peer_name, data)

                time.sleep(sleeptime)

                LoggerClass.spacer(peer_name)


            except socket.error, e:
                AdminManager.email_sender(peer_name,
                                          body="I haven't heard back from node %s in some time." % peer_name,
                                          include_attachment=True)
                print ("Node %s has dropped connection" % peer_name)
                break

    def __init__(self):
        # Variable definitions
        host = 'localhost'
        port = 52000

        connection_counter = 1

        sock = socket.socket()

        """
        The following counter at sock.listen(x) only listens for up to x nodes.
        Increase it to allow for more nodes.
        """

        number_of_nodes = 1
        used_nodes = 0

        sock.bind((host, port))
        sock.listen(number_of_nodes) # This needs to be changed to allow more than 5 nodes!!!

        while True:
            conn, addr = sock.accept()  # Accepting incoming connections
            # Creating new thread. Calling client_thread function for this function and passing conn as argument.
            if used_nodes == number_of_nodes:
                print "The maximum number of nodes has been reached. Please update the config."
                AdminManager.email_sender(peer_name=0,
                                          body="The maximum number of nodes has been reached. "
                                               "Please update the 'number_of_nodes' variable in "
                                               "ConnectionReceiver.__init__.",
                                          include_attachment=False)
            else:
                try:
                    threading.Thread(target=ConnectionReceiver.client_thread, args=(self, connection_counter, conn)).start()
                    connection_counter += 1
                    used_nodes += 1
                except:
                    pass


class LoggerClass:

    """
    Class that logs down the received data from each node. This class contains methods for
    writing all the different info separately.
    """

    def __init__(self, peer_name):
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


class Grapher:

    """Makes a 2D graph out of the gathered data for each node"""

    def __init__(self):
        print "test"


class AdminManager:

    """Notifies the admin of a change in the system, and backs up data to external storage"""

    def __init__(self):
        # The base directories to copy to and from
        from_directory = ''
        to_directory = "/x/y/z"
        # Copies the whole directory
        copy_tree(from_directory, to_directory)

    @staticmethod
    def email_sender(peer_name, body, include_attachment):
        # Simple email sending
        # Tutorial: http://naelshiab.com/tutorial-send-email-python/
        from_addr = "boinc@bsj.sch.id"
        to_addr = "lukas.hejcman@outlook.com"

        msg = MIMEMultipart()

        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = "ADMIN_NOTICE"

        msg.attach(MIMEText(body, 'plain'))

        if include_attachment:
            filename = 'node-%s.log' % peer_name
            attachment = open('node-%s.log' % peer_name, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, 'bertha2016')
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()

ConnectionReceiver()