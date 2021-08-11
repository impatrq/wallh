import socket 
import threading 

HEADER = 64 
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
#print(socket.gethostbyname())

ADDR= (SERVER, PORT)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
FORMAT='utf-8'
DISCONNECT_MENSSAGE="DISCONNECT"


def handle_client(conn, addr): 
    print(f"[Nueva conexion]{addr} conectado.") 
    connected=True 
    while connect:
        msg_length= conn.recv(HEADER).decode(FORMAT) 
        if msg_length:
            msg_length= int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MENSSAGE:
            connect=False

        print(f"[{addr}] {msg}")
        conn.send("Msg_received".encode(FORMAT))

    conn.close()



def start():
  server.listen()
  print(f"[Listening] servidor esta escuchando {SERVER}")
  while True:
    conn, addr= server.accept()
    thread =  threading.Thread(target = handle_client, args= (conn, addr))
    thread.start()
    print(f"[ACTIVE CONECCTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()