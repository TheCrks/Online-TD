import pickle
import socket
from _thread import *
from game import game

server = "(your ip adress here)"
port = 5555

sockett = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sockett.bind((server, port))
except socket.error as e:
    str(e)


sockett.listen()
print("Waiting For Connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(connection, player, gameId):
    global idCount
    connection.send(str.encode(str(player)))

    while True:
        try:
            data = connection.recv(4096).decode()
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(player, data)
                        print("moves: ",game.moves)
                    reply = game
                    connection.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break


    print("Lost Connection")

    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    connection.close()




while True:
    connection, address = sockett.accept()
    print("Connected to : ", address)

    idCount += 1
    player = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = game(gameId)
        print("Creating a new Game ...")
    else:
        games[gameId].ready = True
        player=1


    start_new_thread(threaded_client, (connection, player, gameId))
