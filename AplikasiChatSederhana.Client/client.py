import socket
import threading

# This constant is the same in server. Check it for more information
# HEADER = 16
# PORT = 5050
PORT = 19497

# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '0.tcp.ap.ngrok.io'

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# def formatMsg(msg):
    

#     return 

def listen():
    while True:
        msg = client.recv(128).decode(FORMAT)
        print(f"[BROADCAST] {msg}")

def send(msg):
    # change to binary so the content can actually be sent
    msg = msg.replace(' ',"\r\n") + '\r\n\r\n'
    message = msg.encode(FORMAT)

    # Find the length for the first message (header)
    msg_length = len(message)

    # Padd (tambahin) so the length of the message is 64
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' ' * (HEADER - len(send_length))
    # client.send(send_length)
    client.send(message)


print('Input "DISCONNECTED" to close the program')
str_input = input("Input: ")
thread = threading.Thread(target=listen, daemon=True)
thread.start()

while str_input != "DISCONNECTED":
    str_input = input("Input: ")
    send(str_input)

send(DISCONNECT_MESSAGE)