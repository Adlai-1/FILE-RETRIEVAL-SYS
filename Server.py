# imports...
import configparser
import socket
from cryptography.fernet import Fernet

# open config file...
config = configparser.ConfigParser()
config.read("config.ini")

# necessarry variables...
host = str(config['SERVER']['local'])
port = int(config['SERVER']['port'])
encryptKey = config['SERVER']['key']

crypt = Fernet(encryptKey)

# intializing our server...
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((host, port)) # bind host and port to form a url accessible by clients.
    
    print("Server up!") # indicate if server is running
    
    server.listen() # listen-in for client connection requests

    conn, addr = server.accept() # accepts client connection requests
    print(f"Connection established with {addr}") # show client Ip address

    while True:
        data = conn.recv(1024)
        
        if not data: break # very necesssary to not create an infinite loop...
        
        # open file
        file = open("list.txt", 'r')

        # search algorithm
            # preprocess content obtained from file...
            # search for file name...
        fnames = [itm.strip() for itm in file.readlines()]

        # send feedback to client...
        if data.decode() in fnames:
            conn.send(b"Found")

            # open file and encrypt its content...
            try:
                file = open(data.decode(), 'r').read().encode()
                cnt = crypt.encrypt(file)
                conn.send(cnt)
            except FileNotFoundError:
                conn.send(b"File unavialable")
        else:
            conn.send(b"Not Found")