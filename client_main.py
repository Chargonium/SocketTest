import socket, threading
import sys
import mouse
from time import sleep

MovingRight = False
MovingLeft = False
MovingUp = False
MovingDown = False

ip = input("What is the ip of the server you want to connect to? ")

if ip.lower() == "local" or ip.lower() == "localhost" or ip.lower() == "127.0.0.1":
    ip = socket.gethostbyname(socket.gethostname())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
port = 19131
try:
    sock.connect((ip, port))
except:
    print("Unable to connect to the server")
    sys.exit()
def recieve():
    global MovingRight, MovingLeft, MovingUp, MovingDown
    while True:
        try:
            Message = sock.recv(1024).decode()
            if Message.lower()=="start":
                print("This is just a TEST")
                sock.send("PleaseWork".encode())
            elif Message.lower()=="moveright":
                if MovingRight:
                    MovingRight = False
                else:
                    MovingRight = True
            elif Message.lower()=="moveleft":
                if MovingLeft:
                    MovingLeft = False
                else:
                    MovingLeft = True
            elif Message.lower()=="moveup":
                if MovingUp:
                    MovingUp = False
                else:
                    MovingUp = True
            elif Message.lower()=="movedown":
                if MovingDown:
                    MovingDown = False
                else:
                    MovingDown = True
            elif Message.lower() == "click":
                mouse.click()
                sock.send("Clicked!".encode())
            else:
                print(Message)
        except ConnectionResetError as error:
            print("The server has been closed")
            sleep(5)
            sock.close()
            break

def MouseMoveRight():
    while True:
        if MovingRight:
            x,y = mouse.get_position()
            x += 1
            mouse.move(x,y)
            
        if MovingLeft:
            x,y = mouse.get_position()
            x -= 1
            mouse.move(x,y)

        if MovingUp:
            x,y = mouse.get_position()
            y -= 1
            mouse.move(x,y)
            
        if MovingDown:
            x,y = mouse.get_position()
            y += 1
            mouse.move(x,y)

        sleep(0.00001)

recieve_message_thread = threading.Thread(target=recieve)
mouse_moving_right = threading.Thread(target=MouseMoveRight)

mouse_moving_right.start()
recieve_message_thread.start()