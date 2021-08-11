import socket
import pickle 

SERVER= "192.168.43.180"
HEADER = 64 
PORT = 5050
ADDR = (SERVER, PORT) 
FORMAT='utf-8'
DISCONNECT_MENSSAGE="DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR) 

def send(msg):

  message= msg.encode(FORMAT)
  msg_length= len(message)
  send_length= str(msg_length).encode(FORMAT)
  send_length += b' ' *(HEADER - len(send_length))
  client.send (send_length)
  client.send (client.recv(2048))

send("Hola")
send(DISCONNECT_MENSSAGE)