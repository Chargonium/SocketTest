import socket, threading, pygame,sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
port = 19131
sock.bind(("192.168.68.122", port))
sock.listen(5)

print(f"The ip of this server is: {socket.gethostname()}")
Debounce = False

clients = []

def MovementControls():
    global Debounce

    class Tile(pygame.sprite.Sprite):
        def __init__(self, pos,size,color):
            super().__init__()
            self.image = pygame.Surface((size, size))
            self.image.fill(color)
            self.rect = self.image.get_rect(topleft = pos)

    

    MovementTiles = pygame.sprite.Group()
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                MoveTile = Tile((i * 64 + i + 10,j*64+j + 10), 64, 'black')
                MovementTiles.add(MoveTile)
            else:
                MoveTile = Tile((i * 64+i + 10,j*64+j+10), 64, 'grey')
                MovementTiles.add(MoveTile)
        

    screen_size = (215,215)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Mouse controls")
    clock = pygame.time.Clock()
    
    while True: #run the pygame window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for sprite in MovementTiles.sprites():
            if sprite.rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0]:
                    if not Debounce:
                        broadcast("MoveUp")
                        Debounce = True
                else:
                    if Debounce:
                        broadcast("MoveUp")
                        Debounce = False

        MovementTiles.draw(screen)

        pygame.display.update()
        clock.tick(60)

def broadcast(Message = ''):
    for client in clients:
        client.send(Message.encode())

def handle(client, adress):
    while True:
        try:
            print(client.recv(1024).decode())
        except:
            clients.remove(client)
            print(f"{adress} Has left")
            break

def client_joining():
    while True:
        client, adress = sock.accept()
        clients.append(client)
        print(f"{adress} Connected")
        handling = threading.Thread(target=handle,args=(client,adress,),name=f"Client_{adress[0]}:{adress[1]}")
        handling.start()

def send_message():
    print("What do you want to broadcast?")
    while True:
        message = input("")
        broadcast(message)
    
joining_thread = threading.Thread(target=client_joining,name="Joining_thread")
message_thread = threading.Thread(target=send_message,name="messaging_thread")
pygame_window_thread = threading.Thread(target=MovementControls)

joining_thread.start()
pygame_window_thread.start()
message_thread.start()