import smtplib
import socket


class ConnectionReceiver:

    def __init__(self):
        receive_data()

    def receive_data(self):
        # https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
        self.s = socket.socket()  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        self.port = 12345  # Reserve a port for your service.
        self.s.bind((self.host, self.port))  # Bind to the port
        self.f = open('log', 'wb')
        self.s.listen(5)  # Now wait for client connection.
        while True:
            self.c, self.addr = self.s.accept()  # Establish connection with client.
            print "Got connection from", self.addr
            print "Receiving..."
            self.l = self.c.recv(1024)
            while self.l:
                print "Receiving..."
                self.f.write(self.l)
                self.l = self.c.recv(1024)
            self.f.close()
            print "Done Receiving"
            self.c.send("Thank you for connecting")
            self.c.close()


class ClientTracker:

    def __init__(self):
        add_client()

    def add_client(self):


class AdminNotifier:

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

class BackerUpper:

    def __init__(self):

    def cloud_backer_upper(self):

    def local_backer_upper(self):

