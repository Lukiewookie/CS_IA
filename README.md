# README #

Computer Science IA

### What is this repository for? ###

* This is my Computer Science Internal Assessment v1.0
* Version 1.0

### How do I get set up? ###

* Summary of set up
		
The system works by having one server that takes connections from different nodes by using multithreading. The server creates a thread for every connection that it receives. This thread takes care of receiving the logging data from the node, and writes it downt to a log file called 'node-X.log', where X is the number of the node. This is maintained by the server until such a moment where the connection between the thread and the node is terminated. In such a case, the server sends and email to the pre-determined email address warning the Administrator of this change. 

Furthermore, the server makes mackups of the log files. There is one local file to which the server constantly writes, then there is a separate copy of the file maintained every hour on a separate drive to protect the data from drive failure. Lastly, a copy of the data is kept on the node itself.

* Configuration

number_of_nodes(int) = the limit of how many nodes can connect
to_directory(dir) = the directory to which the backups should be saved
to_addr(str) = the email address to which the email will be sent

* Dependencies

The only dependency for the program in its current state is the psutil module. This can be installed by typing 

```python
pip install psutil
```

The other modules are built into the normal python distribution.

* Deployment instructions

Place the file receiver.py on your server. Preferably somewhere where many files can be created. 
Every node must have a copy of sender.py. This only creates one extra file, so it can be placed almost anywhere.

Firstly, launch the receiver.py, which will start to listen to connection. Make sure that the host for receiver.py is set either to 'localhost', or set the IP manually to the local machine (which can be found through ifconfig).

Each node must be configured to send the data to the receiver by changing the value of the host variable to the IP of the receiver machine. This has to be done for every node, so it is better to do it before the file is duplicated.

### Contribution guidelines ###

* Code review

Currently none. High marks are preffered though :)

* Other guidelines

The code is well commented and clearly written. Everything should be clear. If you want to tinker with it, go wild. But make sure you have a backup copy.

### Who do I talk to? ###

* Repo owner or admim

Lukas Hejcman (lukas.hejcman@outlook.com)

* Other community or team contact

Currently none. After obtaining my IB Diploma, this code will be released on GitHub.