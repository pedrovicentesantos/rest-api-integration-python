import pymysql
import requests
import json
from db_connect import connect_to_db

def get_artist_id(artist):
  try:
    artistId = artistName = ""
    url = "https://itunes.apple.com/search?entity=musicArtist&term=" + artist
    response = requests.get(url)
    if (response.status_code == 200):
      response_json = response.json()
      resultNumber = response_json["resultCount"]
      if(resultNumber == 1):
        artistId = response_json["results"][0]["artistId"]
        artistName = response_json["results"][0]["artistName"]
      elif(resultNumber == 0):
        artistId = artistName = ""
      else:
        for result in response_json["results"]:
          artistName = result["artistName"]
          if (artistName.lower() == artist.lower()):
            artistId = result["artistId"]
            break
      if (not artistId):
        artistName = ""
      return artistId,artistName
  except Exception as e:
	  print(e)

def get_albuns_artist(artist):
  url = "https://itunes.apple.com/lookup?entity=album&id=" + str(artist)
  response = requests.get(url)
  albuns = []
  if (response.status_code == 200):
    response_json = response.json()
    for result in response_json["results"]:
      if (result["wrapperType"] == "collection"):
        albuns.append(result)
  return albuns

def get_songs_artist(artist):
  url = "https://itunes.apple.com/lookup?limit=200&entity=song&id=" + str(artist)
  response = requests.get(url)
  songs = []
  if (response.status_code == 200):
    response_json = response.json()
    for result in response_json["results"]:
      if (result["wrapperType"] == "track"):
        songs.append(result)
  return songs

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