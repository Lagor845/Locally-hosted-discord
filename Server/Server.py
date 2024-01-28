import socket
from threading import Thread
import os

class Server():
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Ip_address = socket.gethostbyname(socket.gethostname())
        self.Port = 34051
        self.server.bind((self.Ip_address,self.Port))
        self.server.listen()
        print(f"[Server] has started at {self.Ip_address}")
        self.rooms = {}
        self.names = []
        self.console = False

    def accept(self):
        while True:
            conn,addr = self.server.accept()
            if self.console == True:
                print(f"[{addr[0]}] has connected...")
            Thread(target=self.server_recv,args=(conn,addr)).start()

    def leave_room(self,client_name,client_joined_room):
        if client_joined_room != "":
            self.rooms[client_joined_room].pop(client_name)
            if len(self.rooms[client_joined_room]) == 0:
                if self.console == True:
                    print(f"[Server] destroying the following room: {client_joined_room}")
                self.rooms.pop(client_joined_room)
    
    def send_msg_to_room(self,conn,msg,client_name,client_joined_room):
        connections = list(self.rooms[client_joined_room].values())
        for connection in connections:
            if connection != conn:
                msg = f"[{client_name}] " + msg + "0x03405"
                msg = msg.encode("utf-8")
                connection.send(msg)

    def server_recv(self,conn,addr):
        client_name = ""
        client_joined_room = ""
        while True:
            try:
                msg = conn.recv(1024).decode("utf-8")
                # Msg formatting is msg+code (No Spaces in between)
                code = msg[-7:]
                msg = msg[:-7]

                # Code meanings are displayed on the right side on the below options
                # Rooms are stored as dictionarys as well as the people inside of them
                # No messages are able to be stored currently, I will probably add an option for that later

                if code == "0x03405": # A message for the currently joined room
                    self.send_msg_to_room(conn,msg,client_name,client_joined_room)


                elif code == "0x00001": # Sends a dud to stop recieving data
                    conn.send("dud".encode("utf-8"))


                elif code == "0x01234": # This sends all available servers to client
                    if self.console == True:
                        print(f"[{addr[0]}] has requested to see rooms...")
                    keys = list(self.rooms.keys())
                    numofkey = len(keys)
                    if numofkey == 0:
                        conn.send(b"0x00000")
                    else:
                        temp = ""
                        if numofkey == 1:
                            temp = keys[0]
                        if numofkey > 1:
                            for key in range(keys):
                                temp = temp + "," + key 
                        temp += "0x16780"
                        size = len(temp)

                        if size <= 1024:
                            conn.send(temp.encode("utf-8"))

                        else:
                            print("sending many")
                            msg = str(size)+"0x00011"
                            conn.send(msg.encode("utf-8"))
                            conn.send(temp.encode("utf-8"))


                elif code == "0x07043": # Creates a new room upon clients request
                    self.rooms[msg] = {client_name : conn}
                    self.leave_room(client_name,client_joined_room)
                    client_joined_room = msg
                    if self.console == True:
                        print(f"[{addr[0]}] created a new room called {msg}...")

                elif code == "0x00868": # The room they wish to join
                    self.leave_room(client_name,client_joined_room)
                    self.rooms[msg][client_name] = conn
                    client_joined_room = msg
                    self.send_msg_to_room(conn,"has joined the session...",client_name,client_joined_room)
                    if self.console == True:
                        print(f"[{addr[0]}] has successfully joined {msg}...")

                elif code == "0x05563": # Sets the clients name
                    used_name = False
                    for i in self.names:
                        if msg == i:
                            used_name=True
                    if used_name == False:
                        if client_name != "":
                            self.names.pop(self.names.index(client_name))
                            oldname = client_name
                        else:
                            oldname = "Default"
                        client_name = msg
                        self.names.append(client_name)
                        conn.send(b"1")
                        if self.console == True:
                            print(f"[{addr[0]}] changed name from [{oldname}] to [{client_name}]...")
                    else: 
                        conn.send(b"0")
                    
            except:
                self.send_msg_to_room(conn,"has disconnected...",client_name,client_joined_room)
                if self.console == True:
                    print(f"[{addr[0]}] has disconnected...")
                self.leave_room(client_name,client_joined_room)
                if client_name != "":
                    self.names.pop(self.names.index(client_name))
                break
                
    def admin_page(self):
        while True:
            main_menu = input(f"Main menu: \n1. View console \n2. View rooms\n3. View conversations \n")
            if main_menu == "1": 
                self.console = True
                while True:
                    maybeinput = input("")
                    if maybeinput == "/exit":
                        break
                self.console = False
            elif main_menu == "2":
                for room in self.rooms:
                    print(room)
                input("")
            elif main_menu == "3":
                pass
            os.system("cls")
                

cool = Server()
Thread(target=cool.accept).start()
cool.admin_page()