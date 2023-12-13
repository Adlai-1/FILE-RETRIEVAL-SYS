# imports...
import configparser
import socket
from cryptography.fernet import Fernet

# config file...
config = configparser.ConfigParser()
config.read("config.ini")

host = str(config['SERVER']['local'])
port = int(config['SERVER']['port'])
encryptKey = config['SERVER']['key']

crypt = Fernet(encryptKey)

# intializing our server...

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, port)) # connect client to Host
    
        while True:

            print("Welcome to your Secure file retrieval system (Press q to exit)")
            data = input("Enter the file name you want...")

            if data.lower() == 'q':
                print("CONNECTION CLOSED!")
                break

            else:
                server.send(data.encode())

            # receieve search feedback
            info = server.recv(1024)
        
            # open file content once its found
            if info.decode() == 'Found':
                info = server.recv(2000)
                if info.decode() == "File unavialable": # Checks to see if the file can be opened or not
                    print("Unable to obtain File content.")
                else:
                    txt = crypt.decrypt(info) # recieve and decrypt file content
                    print(txt.decode()) # show file content to the user.
            else:
                print("SESSION ENDED!")
                break
except:
    print("Client Server Down.")
        
    
