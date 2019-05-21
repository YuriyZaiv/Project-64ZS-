import socket
from _thread import *
import pickle
from game import Game

server = "192.168.0.43"   #Local IP
port = 3535

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("succescful launch:)")

connected = set()
games = {}
idC = 0

def threaded_client(conn, p, gId):
    global idC

    conn.send(str.encode(str(p)))

    reply = " "
    while True:
        try:
            data = conn.recv(4096).decode()
            if gId in games:
                game = games[gId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break

        except:
            break

    print("Lost connection")

    try:
        del games[gId]
        print("Closing Game", gId)
    except:
        pass

    idC -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("connected to:", addr)

    idC += 1
    p = 0
    gId = (idC - 1)//2
    if idC % 2 == 1:
        games[gId] = Game(gId)
        print("creating a new game...)")
    else:
        games[gId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gId))
