import socket
from _thread import start_new_thread
import sys

def read_pos(string):
	string = string.split(",")
	return int(string[0]), int(string[1]), int(string[2]), int(string[3]), str(string[4])

def make_pos(tup):
	return f"{tup[0]}, {tup[1]}, {tup[2]}, {tup[3]}, {tup[4]}"

server = "25.71.127.50"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection...")

pos = [(0, 0, 0, 0, ""), (100, 100, 0, 0, "")]
def threaded_client(conn, currentplayer):
    conn.send(str.encode(make_pos(pos[currentplayer])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[currentplayer] = data

            if not data:
                print("Disconnected")
                break
            else:
                if currentplayer == 1: reply = pos[0]
                else: reply = pos[1]
                print(f"Recieved: {data}")
                print(f"Sending: {reply}")
            
            conn.sendall(str.encode(make_pos(reply)))

        except:
            print("Failed to recieve data")
            break
    
    print("Lost connection")
    conn.close()

currentplayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentplayer))
    currentplayer += 1