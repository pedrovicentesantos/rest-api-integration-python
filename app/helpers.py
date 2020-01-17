import pymysql
from db_connect import connect_to_db
from obterDados import get_artist_id

def on_db(item,table):
  try:
    find = False
    connection = connect_to_db()
    if(table=="artists"):
      # find = False
      sql = "SELECT * FROM artists"
      # connection = connect_to_db()
      if connection.is_connected():
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
          if(row[1].lower() == item['name'].lower()):
            find = True
            break
    
    elif (table=="albuns"):
      sql = "SELECT idAlbumItunes FROM albuns"
      if (connection.is_connected()):
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in rows:
          
          if (row[0] == item):
            find = True
            break
    elif (table == "songs"):
      sql = "SELECT idSongItunes FROM songs"
      if (connection.is_connected()):
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in rows:
          
          if (row[0] == item):
            find = True
            break
    return find
  except Exception as e:
    print("Error: ", e)
  finally:
    if(connection.is_connected()):
      cursor.close()
      connection.close()

def id_on_db(id,table):
  try:
    find = False
    if (table == "artists"):
      sql = "SELECT * FROM artists WHERE idArtist=%s"
    elif (table == "albuns"):
      sql = "SELECT * FROM albuns WHERE idAlbum=%s"
    elif (table == "songs"):
      sql = "SELECT * FROM songs WHERE idSong=%s"
    connection = connect_to_db()
    if connection.is_connected():
      cursor = connection.cursor(pymysql.cursors.DictCursor)
      cursor.execute(sql,(id,))
      row = cursor.fetchone()
      if (not row):
        find = False
      else:
        find = True
    return (find,row)
  except Exception as e:
    print("Error: ", e)
  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()
  


def is_on_itunes(artist):
  onItunes = False
  try:
    id, name = get_artist_id(artist)
    if (not id):
      onItunes = False
    else:
      onItunes = True
    return (onItunes,id,name)
  except Exception as e:
    print("Error:", e)