import pymysql
from app import app
import helpers
from db_connect import connect_to_db
from flask import flash, request, jsonify
import json
from helpers.responses import not_found
from controllers.artist_controller import ArtistController
from controllers.album_controller import AlbumController
from controllers.song_controller import SongController
from repositories.sqlite_repository import SQLiteRepository

repository = SQLiteRepository()

@app.errorhandler(404)
def route_not_found():
    response = not_found('Route not found')
    return response

# Artist routes
@app.route('/artists', methods=['POST'])
def add_artist():
  controller = ArtistController(repository)
  response = controller.add_artist(request)
  return response

@app.route('/artists', methods=['GET'])
def get_artists():
  controller = ArtistController(repository)
  response = controller.get_artists(request)
  return response

@app.route('/artists/<int:index>', methods=['GET'])
def get_artist(index):
  controller = ArtistController(repository)
  response = controller.get_artist(index)
  return response

@app.route('/artists/<int:index>', methods=['PUT'])
def update_artist(index):
  controller = ArtistController(repository)
  response = controller.update_artist(index, request)
  return response
  
@app.route('/artists/<int:index>', methods=['DELETE'])
def delete_artist(index):
  controller = ArtistController(repository)
  response = controller.delete_artist(index)
  return response

@app.route('/artists/<int:index>/albums', methods=['GET'])
def get_artist_albums(index):
  controller = ArtistController(repository)
  response = controller.get_albums(index, request)
  return response

# Album routes
@app.route('/albums', methods=['POST'])
def add_album():
  controller = AlbumController(repository)
  response = controller.add_album(request)
  return response

@app.route('/albums', methods=['GET'])
def get_albums():
  controller = AlbumController(repository)
  response = controller.get_albums(request)
  return response

@app.route('/albums/<int:index>', methods=['GET'])
def get_album(index):
  controller = AlbumController(repository)
  response = controller.get_album(index)
  return response

@app.route('/albums/<int:index>', methods=['PUT'])
def update_album(index):
  controller = AlbumController(repository)
  response = controller.update_album(index, request)
  return response

@app.route('/albums/<int:index>', methods=['DELETE'])
def delete_album(index):
  controller = AlbumController(repository)
  response = controller.delete_album(index)
  return response

# Songs routes
@app.route('/songs', methods=['POST'])
def add_song():
  controller = SongController(repository)
  response = controller.add_song(request)
  return response

@app.route('/songs', methods=['GET'])
def get_songs():
  controller = SongController(repository)
  response = controller.get_songs(request)
  return response

@app.route('/songs/<int:index>', methods=['GET'])
def get_song(index):
  controller = SongController(repository)
  response = controller.get_song(index)
  return response

@app.route('/songs/<int:index>', methods=['PUT'])
def update_song(index):
  controller = SongController(repository)
  response = controller.update_song(index, request)
  return response

@app.route('/songs/<int:index>', methods=['DELETE'])
def delete_song(index):
  controller = SongController(repository)
  response = controller.delete_song(index)
  return response

@app.route('/artistas/<int:index>/albuns', methods=['GET'])
def get_all_albuns_artist(index):
  try:    
    find, _ = helpers.id_on_db(index,"artists")
    if (not find):
      response = "Artist not on DB."
      response = jsonify(response)
      response.status_code = 404
    else:
      connection = connect_to_db()
      sql = "SELECT * FROM albuns WHERE idArtistAlbum=%s"
      if (connection.is_connected()):
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,(index,))
        rows = cursor.fetchall()
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        for row in rows:
          response.append(dict(zip(row_headers,row)))
      response = jsonify(response)
      response.status_code = 200
    return response
  except Exception as e:
    response = jsonify("Error: "+str(e))
    response.status_code = 400
    return response
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index>/musicas', methods=['GET'])
def get_all_songs_artist(index):
  try:
    find, _ = helpers.id_on_db(index,"artists")
    if (not find):
      response = jsonify("Artist not on DB.")
      response.status_code = 404
    else:  
      connection = connect_to_db()
      sql = "SELECT songs.* FROM songs INNER JOIN albuns ON albuns.idArtistAlbum=%s"
      if (connection.is_connected()):
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,(index,))
        rows = cursor.fetchall()
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        for row in rows:
          response.append(dict(zip(row_headers,row)))  
      response = jsonify(response)
      response.status_code = 200
    return response
  except Exception as e:
    reponse = jsonify("Error: "+str(e))
    response.status_code = 400
    return response
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index_artista>/albuns/<int:index_album>',methods=['GET'])
def get_album_artist(index_artista,index_album):
  try:
    find, _ = helpers.id_on_db(index_artista,"artists")
    if (not find):
      response = jsonify("Artist not on DB.")
      response.status_code = 404
    else:
      find, row = helpers.id_on_db(index_album,"albuns")
      if (find):
        # Checa se o album desejado pertence ao artista
        if (row[7] == index_artista):
          response = {
            'idAlbum' : row[0],
            'nameAlbum' : row[1],
            'trackCount' : row[2],
            'explicit' : row[3],
            'genre' : row[4],
            'idAlbumItunes' : row[5],
            'nameArtistAlbum' : row[6],
            'idArtistAlbum' : row[7]
          }
        else:
          response = []
        response = jsonify(response)
        response.status_code = 200
      else:
        response = jsonify("Album not on DB.")
        response.status_code = 404
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response

@app.route('/artistas/<int:index_artista>/musicas/<int:index_musica>',methods=['GET'])
def get_song_artist(index_artista,index_musica):
  try:
    find, _ = helpers.id_on_db(index_artista,"artists")
    if (not find):
      response = jsonify("Artist not on DB.")
      response.status_code = 404
    else:
      find, row = helpers.id_on_db(index_musica,"songs")
      if (find):
        # Checa se a musica pertence a um album que pertence ao artista correto
        findAlbum, rowAlbum = helpers.id_on_db(row[7],"albuns")
        if (findAlbum):
          if (rowAlbum[7] == index_artista):
            response = {
              'idSong' : row[0],
              'nameSong' : row[1],
              'genre' : row[3],
              'explicit' : row[2],
              'idSongItunes' : row[4],
              'nameArtistSong' : row[5],
              'nameAlbumSong' : row[6],
              'idAlbumSong' : row[7]
            }
          else:
            response = []
          response = jsonify(response)
          response.status_code = 200
      else:
        response = jsonify("Song not on DB.")
        response.status_code = 404
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response

@app.route('/albuns',methods=['GET'])
def get_all_albuns():
  try:
    sql = "SELECT * FROM albuns"
    connection = connect_to_db()
    if (connection.is_connected()):
      cursor = connection.cursor(pymysql.cursors.DictCursor)
      cursor.execute(sql)
      rows = cursor.fetchall()
      row_headers = [column_name[0] for column_name in cursor.description]
      response = []
      for result in rows:
        response.append(dict(zip(row_headers,result)))
      response = jsonify(response)
      response.status_code = 200
      return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index>/musicas', methods=['GET'])
def get_songs_album(index):
  try:
    find, _ = helpers.id_on_db(index,"albuns")
    if (not find):
      response = jsonify("Album not on DB.")
      response.status_code = 404
    else:
      connection = connect_to_db()
      sql = "SELECT * FROM songs WHERE idAlbumSong = %s"
      data = (index,)
      if (connection.is_connected()):
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,data)
        rows = cursor.fetchall()
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        for result in rows:
          response.append(dict(zip(row_headers,result)))
      response = jsonify(response)
      response.status_code = 200
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index_album>/musicas/<int:index_musica>',methods=['GET'])
def get_song_album(index_album,index_musica):
  try:
    find, _ = helpers.id_on_db(index_album,"albuns")
    if (not find):
      response = jsonify("Album not on DB.")
      response.status_code = 404
    else:
      find, row = helpers.id_on_db(index_musica,"songs")
      # app.logger.info(find,row)
      if (find and row[7] == index_album):
        response = {
          'idSong' : row[0],
          'nameSong': row[1],
          'genre': row[3],
          'explicit':row[2],
          'idSongItunes':row[4],
          'nameArtistSong':row[5],
          'nameAlbumSong':row[6],
          'idAlbumSong':row[7]
        }
        response = jsonify(response)
        response.status_code = 200
      elif (not find):
        response = jsonify("Song not on DB.")
        response.status_code = 404
      elif (row[7] != index_album):
        response = "Song not from album."
        response = jsonify(response)
        response.status_code = 200
      
      
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
      
@app.route('/albuns/<int:index_album>/musicas/<int:index_musica>',methods=['DELETE'])
def delete_song_album(index_album,index_musica):
  try:
    find,_ = helpers.id_on_db(index_album,"albuns")
    if (not find):
      response = jsonify("Album not on DB.")
      response.status_code = 404
    else:
      findSong, row = helpers.id_on_db(index_musica,"songs")
      if(not findSong):
        response = jsonify("Song not on DB.")
        response.status_code = 404
      else:
        if (row[7] == index_album):
          connection = connect_to_db()
          if (connection.is_connected()):
            sql = "DELETE FROM songs WHERE idSong=%s"
            cursor = connection.cursor()
            cursor.execute(sql,(index_musica,))
            connection.commit()
            response = "Deletion successful."
            response = jsonify(response)
            response.status_code = 200
        else:
          response = "Song not from album."
          response = jsonify(response)
          response.status_code = 200
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (find and findSong and row[7] == index_album and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index>/musicas',methods=['DELETE'])
def delete_songs_album(index):
  try:
    find,_ = helpers.id_on_db(index,"albuns")
    if (not find):
      response = jsonify("Album not on DB.")
      response.status_code = 404
    else:
      connection = connect_to_db()
      sql = "DELETE FROM songs WHERE idAlbumSong=%s"
      if (connection.is_connected()):
        cursor = connection.cursor()
        cursor.execute(sql,(index,))
        connection.commit()
        response = "Deletion successful."
        response = jsonify(response)
        response.status_code = 200
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns', methods=['DELETE'])
def delete_all_albuns():
  try:
    sql = "DELETE FROM albuns"
    connection = connect_to_db()
    if (connection.is_connected()):
      cursor = connection.cursor()
      cursor.execute(sql)
      connection.commit()
      response = jsonify("Deletion successful")
      response.status_code = 200
      return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/musicas', methods=['DELETE'])
def delete_all_songs():
  try:
    sql = "DELETE FROM songs"
    connection = connect_to_db()
    if (connection.is_connected()):
      cursor = connection.cursor()
      cursor.execute(sql)
      connection.commit()
      response = jsonify("Deletion successful")
      response.status_code = 200
      return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

# Rotas iTunes
@app.route('/artistas/<int:index>/albuns/itunes',methods=['GET'])
def get_all_albuns_artist_itunes(index):
  try:    
    find, row = helpers.id_on_db(index,"artists")
    if (not find):
      response = jsonify("Artist not on DB.")
      response.status_code = 404
    else:  
      artistId = row[2]
      if (artistId):
        albuns = helpers.get_type_from_id(artistId, "album")
        if (type(albuns) == str):
          response = jsonify(albuns)
          response.status_code = 400
        else:
          responseDict = []
          for album in albuns:
            responseDict.append(
              {
                'nameArtistAlbum' : album['artistName'],
                'nameAlbum' : album['collectionName'],
                'trackCount' : album['trackCount'],
                'explicit' : album['collectionExplicitness'],
                'genre' : album['primaryGenreName'],
                'idAlbumItunes' : album['collectionId']
              }
            )
          response = jsonify(responseDict)
          response.status_code = 200
      else:
        response = jsonify("Artist not on iTunes.")
        response.status_code = 200
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response

@app.route('/artistas/<int:index>/musicas/itunes', methods=['GET'])
def get_all_songs_artist_itunes(index):
  try:
    find, row = helpers.id_on_db(index,"artists")
    if (not find):
      response = jsonify("Artist not on DB.")
      response.status_code = 404
    else:  
      artistId = row[2]
      if (artistId):
        songs = helpers.get_type_from_id(artistId, "song")
        if (type(songs) == str):
          response = jsonify(songs)
          response.status_code = 400
        else:
          responseDict = []
          for song in songs:
            responseDict.append(
              {
                'nameArtistSong' : song['artistName'],
                'nameAlbumSong' : song['collectionName'],
                'nameSong' : song['trackName'],
                'explicit' : song['trackExplicitness'],
                'genre' : song['primaryGenreName'],
                'idSongItunes' : song['trackId']
              }
            )
          response = jsonify(responseDict)
          response.status_code = 200
      else:
        response = jsonify("Artist not on iTunes.")
        response.status_code = 200
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response

@app.route('/albuns/<int:index>/musicas/itunes', methods=['GET'])
def get_all_songs_album_itunes(index):
  try:
    find, row = helpers.id_on_db(index,"albuns")
    if (not find):
      response = jsonify("Album not on DB.")
      response.status_code = 404
    else:  
      albumId = row[5]
      if (albumId):
        songs = helpers.get_type_from_id(albumId, "song")
        if (type(songs) == str):
          response = jsonify(songs)
          response.status_code = 400
        else:
          responseDict = []
          for song in songs:
            responseDict.append(
              {
                'nameArtistSong' : song['artistName'],
                'nameAlbumSong' : song['collectionName'],
                'nameSong' : song['trackName'],
                'explicit' : song['trackExplicitness'],
                'genre' : song['primaryGenreName'],
                'idSongItunes' : song['trackId']
              }
            )
          response = jsonify(responseDict)
          response.status_code = 200
      else:
        response = jsonify("Album not on iTunes.")
        response.status_code = 200
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response



if __name__ == '__main__':
  app.run(debug=True,host = '0.0.0.0')
