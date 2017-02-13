import psutil
import socket


class Node:

    def __init__(self):
        DataGatherer()
        FileManager()
        ConnectionSender()
        DataSaver()


class DataGatherer:

    def __init__(self):
        FileManager()
        self.gather_data()

    def gather_data(self):
        # Gathering information about CPU Usage
        self.cpu_usage = psutil.cpu_percent(FileManager.update_time, False) # (Time period, Multicore?)
        # Gathering info about SWAP usage
        self.ram_usage = psutil.virtual_memory()


class FileManager:

    def __init__(self):
        self.file_loader()
        self.file_saver()
        self.read_preferences()

    def file_loader(self):
        # Loading log files
        try:
            self.log = open('log', 'w')
        except IOError:
            print 'Cannot open log.txt'

        # Loading config files
        self.config = open('config', 'w')

    def file_saver(self):
        # Writing to the log file
        self.log.write("Date and time:  CPU Usage:   RAM Usage")
        self.log.write('\n')
        self.log.write(DataGatherer.cpu_usage)
        self.log.write('   ' + DataGatherer.ram_usage)

    def read_preferences(self):
        # Taking important info from file
        self.node_name = self.config.readline(2)
        self.update_time = self.config.readline(5)
        self.receivers = self.config.read_line(8)
        self.port = self.config.readline(11)


class ConnectionSender:

    def __init__(self):
        self.data_sender()
        self.find_receivers()

    def data_sender(self):
        # https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
        self.s = socket.socket()  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        self.port = 12345  # Reserve a port for your service.

        self.s.connect((host, port))
        self.f = open('tosend.png', 'rb')
        print 'Sending...'
        self.l = self.f.read(1024)
        while (self.l):
            print 'Sending...'
            self.s.send(self.l)
            self.l = self.f.read(1024)
        self.f.close()
        print "Done Sending"
        self.s.shutdown(socket.SHUT_WR)
        print s.recv(1024)
        self.s.close  # Close the socket when done


