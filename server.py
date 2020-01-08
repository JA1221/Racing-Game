import socket
from _thread import *
import pickle
from game import Game

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0
waitingNum = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            # 遊戲房間還在
            if gameId in games:
                game = games[gameId]

                # 沒有資料(斷開連線)
                if not data:
                    break
                # 接收到資料
                else:
                    # 重設
                    if data == "reset":
                        game.resetWent()
                    # 取得物件(玩家幾, 資料)
                    elif data != "get":
                        game.play(p, data)

                    # 傳送game物件
                    conn.sendall(pickle.dumps(game))
            # 遊戲房間消失
            else:
                break
        # 連線意外
        except:
            break

    print("Lost connection")
    # 刪除房間
    try:
        del games[gameId]
        print("Closing Game", gameId)
    # 房間已關閉
    except:
        print()
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr, "idCount", idCount)

    # 總共有幾位連線
    idCount += 1
    # 玩家幾 0 or 1
    p = 0
    # 房間號碼
    gameId = (idCount - 1)//2
    
    # 玩家1加入 開啟新遊戲
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    # 玩家1加入
    else:
        games[gameId].ready = True
        p = 1
        print("Game Start!!!\n")


    start_new_thread(threaded_client, (conn, p, gameId))
