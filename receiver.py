#!/usr/bin/python
import smtplib
import socket
import logging
import time
import threading
import dropbox

from distutils.dir_util import copy_tree

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


class ConnectionReceiver:

    """Gets data from each client by creating a thread for each of them"""

    @staticmethod
    def client_thread(conn):

        peer_name = conn.recv(1024)
        time.sleep(0.1)

        threading.Thread(target=LoggerClass, args=(peer_name,)).start()
        # Sets the amount of time between the different connection. Change this to change the frequency of logging
        sleeptime = 0.1
        # infinite loop so that function do not terminate and thread do not end.
        while True:

            try:  # Error handling
                # Receiving from client
                data = conn.recv(1024)  # Receive 1024 bytes of data
                print("%s CPU: %s" % (peer_name, data))
                LoggerClass.cpu_log(peer_name, data)  # Log it to file

                time.sleep(sleeptime)  # wait for the other transmissions

                data = conn.recv(1024)
                print("%s RAM: %s" % (peer_name, data))
                LoggerClass.ram_log(peer_name, data)

                time.sleep(sleeptime)

                data = conn.recv(1024)
                print("%s DISK: %s" % (peer_name, data))
                LoggerClass.disk_log(peer_name, data)

                time.sleep(sleeptime)

                data = conn.recv(1024)
                print("%s SENT: %s" % (peer_name, data))
                LoggerClass.netsent_log(peer_name, data)

                time.sleep(sleeptime)

                data = conn.recv(1024)
                print("%s RECV: %s" % (peer_name, data))
                LoggerClass.netrecv_log(peer_name, data)

                time.sleep(sleeptime)

                LoggerClass.spacer(peer_name)

                try:
                    if time.time() % 3600 == 0:
                        AdminManager.file_uploader(upload_file_from='C:\Users\Lukáš Hejcman\PycharmProjects\CS_IA\node-%s.log' % peer_name,
                                                   upload_file_to='CS_IA\node-%s.log' % peer_name)
                except:
                    print("Was unable to upload file. Backed up to local storage instead.")
                    AdminManager.local_backer(from_directory='C:\Users\Lukáš Hejcman\PycharmProjects\CS_IA\node-%s.log' % peer_name,
                                              to_directory='C:\Users\Lukáš Hejcman\Desktop\node-%s.log' % peer_name)

            except socket.error:
                AdminManager.email_sender(peer_name,
                                          subject="%s_UNRESPONSIVE" % peer_name,
                                          body="I haven't heard back from node '%s' in some time." % peer_name,
                                          include_attachment=True)
                print ("Node '%s' has dropped connection" % peer_name)
                break

    def __init__(self):
        # Variable definitions
        host = 'localhost'
        port = 52000

        sock = socket.socket()

        """
        The following counter at sock.listen(x) only listens for up to x nodes.
        Increase it to allow for more nodes.
        """

        number_of_nodes = 1
        used_nodes = 0

        sock.bind((host, port))
        sock.listen(number_of_nodes)  # This needs to be changed to allow more than 5 nodes!!!

        while True:
            conn, addr = sock.accept()  # Accepting incoming connections
            # Creating new thread. Calling client_thread function for this function and passing conn as argument.
            if used_nodes == number_of_nodes:
                print "The maximum number of nodes has been reached. Please update the config."
                AdminManager.email_sender(peer_name=0,
                                          subject="ADMIN_NOTICE",
                                          body="The maximum number of nodes has been reached. "
                                               "Please update the 'number_of_nodes' variable in "
                                               "ConnectionReceiver.__init__.",
                                          include_attachment=False)
            else:
                try:
                    threading.Thread(target=ConnectionReceiver.client_thread, args=(conn,)).start()
                    used_nodes += 1
                except socket.error:
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
        logger.info("CPU Used: %s (for each core)" % data)

    @staticmethod
    def ram_log(peer_name, data):
        # Log RAM data
        logger = logging.getLogger('node-%s' % peer_name)
        logger.info("RAM Used: %s PRC", data)

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
        print "WIP"


class AdminManager:

    """Notifies the admin of a change in the system, and backs up data to external storage"""

    def __init__(self):
        print("The admin manager is active now")

    @staticmethod
    def local_backer(from_directory, to_directory):
        #copies the whole directory
        copy_tree(from_directory, to_directory)

    @staticmethod
    def file_uploader(upload_file_from, upload_file_to):
        # https://stackoverflow.com/questions/23894221/upload-file-to-my-dropbox-from-python-script
        # Takes the file and uploads it to Dropbox
        dbx = dropbox.Dropbox('nzvJcwuTbfAAAAAAAAAAJ_GLQaaITMigKEA6M6w7ouvgjElJ5fd4_nrgbyQNaQEs')
        print(dbx.users_get_current_account())

        with open(upload_file_from, 'rb') as f:
            dbx.files_upload(f.read(), upload_file_to)

    @staticmethod
    def email_sender(peer_name, subject, body, include_attachment):
        # Simple email sending
        # Tutorial: http://naelshiab.com/tutorial-send-email-python/
        from_addr = "boinc@bsj.sch.id"
        to_addr = "lukas.hejcman@outlook.com"

        msg = MIMEMultipart()

        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject

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
