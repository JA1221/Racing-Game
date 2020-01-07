import mysql.connector

con = mysql.connector.connect(
    host="35.201.248.77",
    user="game",
    passwd="game123",
    database="game"
)

cursor = con.cursor()

def user_signup(tup):#註冊使用者
    try:
        cursor.execute("INSERT INTO player(user_id, user_name, password) VALUES(%s,%s,%s)", tup)
        return True
    except:
        return False

def user_login(tup):#登入查詢
    try:
        cursor.execute("SELECT * FROM player WHERE user_id=%s AND password=%s", tup)
        return (cursor.fetchone())
    except:
        return False

def user_last():#搜尋最後註冊者
    try:
        cursor.execute("SELECT * FROM player ORDER BY player.user_id DESC Limit 1")
        return (cursor.fetchall())
    except:
        return False

def all_score():#總成績排名
  try:
      cursor.execute("SELECT * FROM score ORDER BY score.score DESC Limit 5")
      return (cursor.fetchall())
  except:
      return False

def insert_score(tup):#登入成績
    try:
        cursor.execute("INSERT INTO score(user_id, score, time) VALUES(%s,%s,%s)", tup)
        return True
    except:
        return False