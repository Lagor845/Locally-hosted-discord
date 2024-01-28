import socket
from threading import Thread
import os

# Here is the full explanation for all of the codes

# SERVER SIDE
# 0x03405 : Messages for the currently joined room
# 0x00001 : Dud to kill recv thread
# 0x01234 : Ask to recv rooms
# 0x07043 : Tells the server to create a new room upon clients request
# 0x00868 : Tells the server which room the client would like to join
# 0x05563 : This sets the name of the client on the server

# CLIENT SIDE
# 0x00011 : This tells the client that they are going to recv more than 1024 bytes of information
# 0x00000 : A security measure to make sure the client knows if it should be recieving rooms or not


class Server():
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Ip_address = None
        self.Port = 34051 
        self.addr = (self.Ip_address,self.Port)
        self.servers = []
        self.name = None
        self.current_room = ""


    def send_dud(self):
        self.server.send("0x00001".encode("utf-8"))


    def Set_name(self):
        while True:
            self.name = input("What do you want your name to be? \n")
            os.system("cls")
            msg = self.name+"0x05563"
            self.server.send(msg.encode("utf-8"))
            if self.server.recv(8).decode("utf-8") == "1":
                input("Name successfully set \n")
                os.system("cls")
                break
            else:
                input("Name is not availble! \n")
                os.system("cls")


    def Connect_to_server(self):
        count = 0
        failed = True
        while True:
            try:
                joined = self.server.connect_ex((self.Ip_address,self.Port))
                if joined == 0:
                    failed = False
                    break
                else:
                    if count == 3:
                        print("Connection failed!!!")
                        break
                    else:
                        count += 1
            except:
                print("Connection failed!!!")
        return failed
    

    def Join_server(self):
        while True:
            self.Ip_address = input("Server Ip address: ")
            os.system("cls")
            if self.Connect_to_server() == False:
                input("Connected sucessfully!!! \n")
                os.system("cls")
                break
            os.system("cls")


    def create_new_room(self,dialoge):
        room_name = input(dialoge)
        os.system("cls")
        msg = room_name+"0x07043"
        self.current_room = room_name
        self.server.send(msg.encode("utf-8"))


    def Join_room(self):
        self.server.send(b"0x01234") # Requests all rooms from client
        msg = self.server.recv(1024).decode("utf-8") # Recives either a either a number of bits or the rooms names
        code = str(msg[-7:])
        msg = msg[:-7]
        msg = str(msg)
        if code == "0x00011":
            msg = self.server.recv(int(msg)).decode("utf-8")
            code = msg[-7:]
            msg = str(msg[:-7]) 
        self.servers = msg.split(",")
        numofroom = len(self.servers)
        if code != "0x00000":
            while True:
                temp = "Which room do you want to join?"
                servers = False
                for num in range(numofroom):
                    if self.servers[num] != self.current_room:
                        temp += "\n"+str(num)+". "+self.servers[num]
                        servers = True
                if servers == True:
                    temp+="\n"
                    choice = int(input(temp))
                    try:
                        server = self.servers[choice]
                        self.current_room = server
                        server += "0x00868"
                        self.server.send(server.encode("utf-8"))
                        os.system("cls")
                        break
                    except:
                        input("Not a valid value")
                else:
                    choice = input("No other servers are currently available! Your options are: \n1. Stay in current room \n2. Create new room \n")
                    if choice == "1":
                        os.system("cls")
                        break
                    elif choice == "2":
                        self.create_new_room("What would you like to name the new room? \n")
                os.system("cls")
        else:
            self.create_new_room("No rooms on the server! Create your own! What would you like to name it? \n")


    def send(self):
        print(f"You are currently communicating in {self.current_room}")
        while True:
            msg = input("")
            if msg == "":
                break
            else:
                msg = msg+"0x03405"
                self.server.send(msg.encode("utf-8"))
        os.system("cls")
        self.send_dud()
        

    def receive(self):
        while True:
            msg = self.server.recv(1024).decode("utf-8")
            code = msg[-7:]
            msg = msg[:-7]
            if code == "0x03405":
                print(msg)
                
            elif code == "dud":
                break


    def start_conversing(self):
        Thread(target=self.receive).start()
        self.send()


    def main_menu(self):
        while True:
            options = input(f"Main Menu: \n1. Messages \n2. Change Room (Current: {self.current_room}) \n3. Change Name (Current: {self.name}) \n")
            os.system("cls")
            if options == "1":
                self.start_conversing()
            elif options == "2":
                self.Join_room()
            elif options == "3":
                self.Set_name()


def main():
    cool = Server()
    cool.Join_server()
    cool.Set_name()
    cool.Join_room()
    Thread(target=cool.receive).start()
    cool.send()
    cool.main_menu()
    

main()