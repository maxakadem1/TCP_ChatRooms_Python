#Maxim ABdbdulkhalikov
#7876165
#COMP4300 Assignment 1 
#=======================
#Server file that hosts all the clients for communication
#=======================
#To lauch a file, open in in cmd/powershell and write "python3 server.py".
#It will host the server on HOST: 127.0.0.1 and PORT: 4073 (can be changed in variables if needed)


#imports
import sys
import socket
import threading

class Server:

    #format for messages
    FORMAT = "utf-8"
    HOST = "127.0.0.1"
    PORT = 4073
    
    #instructions text that is sent to the client
    greetingText = "\n---Welcome to the chat server---\n" + "<-commands> to print this command menu again\n" + "<-join> <roomname> to join a room. If room does not exist it will be created\n"+ "<-room> displays your current room\n" + "<-roomlist> to display all the rooms\n"\

    #creating a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #server init function
    def __init__(self,addr):
        self.server.bind(addr)
        self.server.listen()
        #making rooms a dictionary type for all rooms and their clients 
        self.rooms = {} 
        self.listOfClients = []
        self.nicknames = []

    #send a message to all clients
    def sendToAll(self,client,message,roomName):
        if roomName in self.rooms:
            for eachClient in self.rooms[roomName]:
                    eachClient.send(message)
                    
    #remove a client from a room
    def removeClient(self,client):
        for room in self.rooms:
            if client in self.rooms[room]:
                self.rooms[room].remove(client)
                break
   
    #add a client to a room (-join command)
    def addClient(self,client, nickname, roomName):
        #check if he is not in the room already
        if client not in self.rooms[roomName]:
            #remove the client from the old room
            self.removeClient(client)
            self.rooms[roomName].append(client)
            print(nickname + " joined room " + roomName)

            #informing everyone that a new peron joined the room
            #exception for a person himself, different message
            for person in self.rooms[roomName]:
                if person == client:
                    client.send("You joined  {}".format(roomName).encode(self.FORMAT))
                else:
                    person.send("{} joined {}".format(nickname,roomName).encode(self.FORMAT))
        #if there is 5 people in the room, inform the client that he cannot join
        elif len(self.rooms[roomName]) > 5:
            client.send("Room is full".encode(self.FORMAT))
        else:
            client.send("{} tried to join a room he is already in".format(nickname).encode(self.FORMAT))

    #create a new room and join it
    def createRoom(self, roomName, nickname, client):
        #removing a client from the old room so he can join the new one
        self.removeClient(client)
        #creating and joining the new room
        self.rooms[roomName] = [client]
        print(nickname + " created and joined room " + roomName)

    def listAllRooms(self,client):
        message = "\nRooms:\n"
        for room in self.rooms:
            #list all users in the room
            names = [self.nicknames[self.listOfClients.index(person)] for person in self.rooms[room]]
            message += "{} [{}/5][{}] \n".format(room, len(self.rooms[room]), names)
        client.send(message.encode(self.FORMAT))
    
    #function for showing a current room for the client (-room command)
    def currentRoom(self,client):
        for room in self.rooms:
            if client in self.rooms[room]:
                client.send("You are currently in : {}".format(room).encode(self.FORMAT))
                break

    #function that handles client interaction (commands and sending messages)
    def clientInteraction(self,client,roomName):
        while True:
            try:
                message = client.recv(1024)

                #determining the command in the message, default case starts with a message that user wants to send
                messageParts = message.decode(self.FORMAT).split()

                if len(messageParts) <= 1:
                    client.send("Please enter message".encode(self.FORMAT))

                elif len(messageParts) > 100:
                    client.send("Message is too long".encode(self.FORMAT))

                #handling the commands
                elif(messageParts[1] == "-commands"):
                    client.send(self.greetingText.encode(self.FORMAT))
                elif(messageParts[1] == "-join"):
                    nickname = messageParts[0][:-1]
                    roomName = messageParts[2]
                    if(roomName not in self.rooms):
                        self.createRoom(roomName, nickname, client)
                    else:
                        self.addClient(client, nickname, roomName)
                elif(messageParts[1] == "-room"):
                    self.currentRoom(client)
                elif(messageParts[1] == "-roomlist"):
                    self.listAllRooms(client)
                else:
                    self.sendToAll(client, message,roomName)
            except:
                #deleting client as he is no longer able to send messages
                index = self.listOfClients.index(client)
                self.listOfClients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                #removing nickname from the list
                print(self.nicknames[index] + " has left the server")
                
                self.removeClient(client)
                self.nicknames.remove(nickname)
                break

    def mainAddition(self):
        while True:
            #adding a client to a server
            client, addr = self.server.accept()
            print("Connection occured from {}".format(str(addr)))
            #getting data from the client to add to the list of clients
            client.send("getData".encode(self.FORMAT))

            response = client.recv(1024).decode(self.FORMAT)
            splitRepsonse = response.split()
            nickname = splitRepsonse[0]
            roomName = splitRepsonse[1]

            #check if room exists
            if(roomName in self.rooms):
                self.rooms[roomName].append(client)
                for person in self.rooms[roomName]:
                    person.send("{} joined this room!".format(nickname).encode(self.FORMAT))
            else:
                #if no, create it and join
                self.createRoom(roomName, nickname, client)
                print("user {} created and joined room {}".format(nickname,roomName))

            print("New clients nickname is {}".format(nickname))
            client.send("Welcome to my little chat server! Hope you dont encounter any bugs!\nPlease read the instructions below to start or just type your messages if you are already in a correct room!".encode(self.FORMAT))
            client.send(self.greetingText.encode(self.FORMAT))

            #adding his info to the list
            self.nicknames.append(nickname)
            self.listOfClients.append(client)

            #threads for each client
            thread = threading.Thread(target=self.clientInteraction,args=(client,roomName,))
            thread.start()


def main():
    ADDRESS = ('127.0.0.1',4073)
    s = Server(ADDRESS)
    print("Server started")
    s.mainAddition()
        

if __name__ == "__main__":
    main()