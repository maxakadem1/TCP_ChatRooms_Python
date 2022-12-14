#Maxim ABdbdulkhalikov
#7876165
#COMP4300 Assignment 1 
#=======================
#Client file that creates a new client to connect to the server
#=======================
#To lauch a file, open in in cmd/powershell and write "python3 client.py <name> <chanelname>"
#If the chanel does not exist, it will be created, otherwise you will be connected to chanel

#imports
import socket
import sys
import threading



#client class
class Client:
    #format for messages
    FORMAT = "utf-8"
    HOST = "127.0.0.1"
    PORT = 4073
    

    #creating a socket for client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #initializing
    #name of a client, chanel , client adress
    def __init__(self, name, addr, chnl):
        self.name = name
        self.channel = chnl
        self.client.connect(addr)

    #function for sending messages to a server
    def writeToServer(self):
        while True:
            #name input
            userInput = input()
            message = "{}: {}".format(self.name, userInput)

            #send name to server
            self.client.send(message.encode(self.FORMAT))

    def receiveFromServer(self):
        while True:
            try:
                #recieve a message from server
                message = self.client.recv(1024).decode(self.FORMAT)

                #if the message contains a keyword "+getName+Channel", send name and channel to server
                if message == "getData":
                    self.client.send(("{} {}").format(self.name,self.channel).encode(self.FORMAT))
                else:
                #print message if it doest have a code word as usual
                    print(message)

            except:
                print(f"ERROR OCCURED")
                self.client.close()
                break

def main():
    #taking inputs from the user on launch
    #write an error if input is incorrect
    #INPUT: NAME, CHANELNAME
    try:
        nickname, chanel = sys.argv[1], sys.argv[2]
    except:
        print("Not valid input. Please enter your name and chanel name.")
        sys.exit()

    #creating a client
    ADDR = ("127.0.0.1",4073)
    client = Client(nickname, ADDR, chanel)

    #creating threads for writing and listenting
    #recieve thread
    receiveThread = threading.Thread(target=client.receiveFromServer)
    receiveThread.start()

    #write thread
    writeThread = threading.Thread(target=client.writeToServer)
    writeThread.start()

if __name__ == "__main__":  
    main()