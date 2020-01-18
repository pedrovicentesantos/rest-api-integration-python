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
      resultCount = response_json["resultCount"]
      if (resultCount != 0):
        for result in response_json["results"]:
          artistName = result["artistName"]
          if (artistName.lower() == artist.lower()):
            artistId = result["artistId"]
            break
    return artistId,artistName
  except Exception as e:
	  # print("Error: ",e)
    return "Error: " + str(e)

def get_type_from_id(id, searchType):
  try:
    url = "https://itunes.apple.com/lookup?limit=200&entity=" + searchType
    url += "&id="
    url += str(id)
    response = requests.get(url)
    result = []
    if (response.status_code == 200):
      response_json = response.json()
      for item in response_json["results"]:
        if (searchType == "album"):
          if (item["wrapperType"] == "collection"):
            result.append(item)
        elif (searchType == "song"):
          if (item["wrapperType"] == "track"):
            result.append(item)
    return result
  except Exception as e:
    print("Error: ",e)

def on_db(item,table):
  try:
    find = False
    connection = connect_to_db()
    if(table=="artists"):
      sql = "SELECT * FROM artists"
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
    result = get_artist_id(artist)
    if (type(result) == str):
      return (onItunes,result,"")
    if (result[0]):
      onItunes = True
    return (onItunes,result[0],result[1])
  except Exception as e:
    print("Error:", e)