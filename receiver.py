#!/usr/bin/python
import smtplib
import socket
import logging
import time
import threading

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

        # infinite loop so that function do not terminate and thread do not end.
        while True:

            try:  # Error handling
                # Receiving from client
                data = conn.recv(1024)  # Receive 1024 bytes of data
                print data
                LoggerClass.cpu_log(peer_name, data)  # Log it to file

                time.sleep(0.1)  # wait for the other transmissions

                data = conn.recv(1024)
                print data
                LoggerClass.ram_log(peer_name, data)

                time.sleep(0.1)

                data = conn.recv(1024)
                print data
                LoggerClass.disk_log(peer_name, data)

                time.sleep(0.1)

            except socket.error, e:
                AdminManager.email_sender(peer_name)
                print ("The node %s has dropped connection" % peer_name)
                break

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
        logger.info("CPU Used: %s percent" % data)

    @staticmethod
    def ram_log(peer_name, data):
        # Log RAM data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("RAM Used: %s percent", data)

    @staticmethod
    def disk_log(peer_name, data):
        # Log RAM data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("DISK Used: %s MB", data)


class Grapher:

    """Makes a 2D graph out of the gathered data for each node"""




class AdminManager:

    """Notifies the admin of a change in the system, and back up data to external storage"""

    def __init__(self):

        """
        Backup data ye?
        """

    @staticmethod
    def email_sender(peer_name):
        # Simple email sending
        # Tutorial: http://naelshiab.com/tutorial-send-email-python/
        from_addr = "boinc@bsj.sch.id"
        to_addr = "lukas.hejcman@outlook.com"

        msg = MIMEMultipart()

        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = "ADMIN_NOTICE"

        body = "I haven't heard from node %s" % peer_name

        msg.attach(MIMEText(body, 'plain'))

        filename = 'node-%s.log' % peer_name
        attachment = open('node-%s.log' % peer_name, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
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