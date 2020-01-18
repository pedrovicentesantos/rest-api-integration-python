import pymysql
from app import app
import helpers
from db_connect import connect_to_db
from flask import flash, request, jsonify
import json

@app.errorhandler(404)
def page_not_found(e):
    response = "Page not found."
    response = jsonify(response)
    response.status_code = 404
    return response

@app.route('/artistas', methods=['GET'])
def get_artists():
  try:
    sql = "SELECT * FROM artists"
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
    print("Error: ", e)
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index>', methods=['GET'])
def get_artist(index):
  try:
    connection = connect_to_db()
    sql = "SELECT * FROM artists WHERE idArtist=%s"
    if (connection.is_connected()):
      cursor = connection.cursor(pymysql.cursors.DictCursor)
      cursor.execute(sql,(index,))
      row = cursor.fetchone()
      if (not row):
        response = "Artist not on DB."
      else:
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        response.append(dict(zip(row_headers,row)))
      response = jsonify(response)
      response.status_code = 200
      return response
  except Exception as e:
    return jsonify("Error: ", e)
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index>', methods=['PUT'])
def update_artist(index):
  try:
    artist = request.get_json()
    if (not artist):
      response = jsonify("No Body in request.")
    else:
      find, _ = helpers.id_on_db(index,"artists")
      if (not find):
        response = jsonify("Artist not on DB.")
      else:
        result = helpers.is_on_itunes(artist['name'])
        if (type(result) == str):
          response = jsonify(result)
        else:
          connection = connect_to_db()
          if (connection.is_connected()):
            cursor = connection.cursor()
            if (not result[0]):
              id = None
              name = artist['name']
            else:
              id = result[1]
              name = result[2]
            findNameArtist = helpers.on_db(artist,"artists")
            if (not findNameArtist):
              sql = "UPDATE artists SET nameArtist = %s, idArtistItunes=%s WHERE idArtist= %s"
              data = (name,id,index)
              cursor.execute(sql,data)
              connection.commit()
              response = jsonify("Update successful.")  
            else:
              response = jsonify("Artist already on DB.")  
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (artist and find and type(result) != str and connection.is_connected()):
      cursor.close()
      connection.close()
  
@app.route('/artistas/<int:index>', methods=['DELETE'])
def delete_artist(index):
  try:
    find, _ = helpers.id_on_db(index,"artists")
    if (not find):
      response = jsonify("Artist not on DB.")
    else:    
      sql = "DELETE FROM artists WHERE idArtist = %s"
      connection = connect_to_db()
      if (connection.is_connected()):
        cursor = connection.cursor()
        cursor.execute(sql,(index,))
        connection.commit()
        response = jsonify("Deletion successful.")
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas', methods=['POST'])
def add_artist():
  try:
    artist = request.get_json()
    if (not artist):
      response = jsonify("No Body in request.")
    else:
      connection = connect_to_db()
      cursor = connection.cursor()
      find = helpers.on_db(artist,"artists")
      if (find):
        response = jsonify("Artist already on DB.")
      else:
        result = helpers.is_on_itunes(artist['name'])
        if (type(result) == str):
          response = jsonify(result)
        else:
          if (not result[0]):
            id = None
            name = artist['name']
          else:
            id = result[1]
            name = result[2]
          if (connection.is_connected()):
            sql = "INSERT INTO artists (nameArtist,idArtistItunes) VALUES (%s,%s)"
            data = (name,id)
            cursor.execute(sql,data)
            connection.commit()
            response = jsonify("Added successful.")
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (artist and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index>/albuns', methods=['GET'])
def get_all_albuns_artist(index):
  try:    
    find, _ = helpers.id_on_db(index,"artists")
    if (not find):
      response = "Artist not on DB."
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
    print("Error: ", e)
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index>/musicas', methods=['GET'])
def get_all_songs_artist(index):
  try:
    find, _ = helpers.id_on_db(index,"artists")
    if (not find):
      response = "Artist not on DB."
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
    print("Error: ", e)
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index_artista>/albuns/<int:index_album>',methods=['GET'])
def get_album_artist(index_artista,index_album):
  try:
    find, _ = helpers.id_on_db(index_artista,"artists")
    if (not find):
      response = "Artist not on DB."
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
      else:
        response = "Album not on DB."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)

@app.route('/artistas/<int:index_artista>/musicas/<int:index_musica>',methods=['GET'])
def get_song_artist(index_artista,index_musica):
  try:
    find, _ = helpers.id_on_db(index_artista,"artists")
    if (not find):
      response = "Artist not on DB."
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
              'genre' : row[2],
              'explicit' : row[3],
              'idSongItunes' : row[4],
              'nameArtistSong' : row[5],
              'nameAlbumSong' : row[6],
              'idAlbumSong' : row[7]
            }
          else:
            response = []
      else:
        response = "Song not on DB."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)

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
    print("Error: ", e)
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/musicas',methods=['GET'])
def get_all_songs():
  try:
    sql = "SELECT * FROM songs"
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
    print("Error: ", e)
  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index>', methods=['GET'])
def get_album(index):
  try:
    connection = connect_to_db()
    sql = "SELECT * FROM albuns WHERE idAlbum=%s"
    if (connection.is_connected()):
      cursor = connection.cursor(pymysql.cursors.DictCursor)
      cursor.execute(sql,(index,))
      row = cursor.fetchone()
      if (not row):
        response = "Album not on DB."
      else:
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        response.append(dict(zip(row_headers,row)))
      response = jsonify(response)
      response.status_code = 200
      return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/musicas/<int:index>', methods=['GET'])
def get_song(index):
  try:
    connection = connect_to_db()
    sql = "SELECT * FROM songs WHERE idSong=%s"
    if (connection.is_connected()):
      cursor = connection.cursor(pymysql.cursors.DictCursor)
      cursor.execute(sql,(index,))
      row = cursor.fetchone()
      if (not row):
        response = "Song not on DB."
      else:
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        response.append(dict(zip(row_headers,row)))
      response = jsonify(response)
      response.status_code = 200
      return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index>/musicas', methods=['GET'])
def get_songs_album(index):
  try:
    find, _ = helpers.id_on_db(index,"albuns")
    if (not find):
      response = "Album not on DB."
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
    print("Error: ", e)
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index_album>/musicas/<int:index_musica>',methods=['GET'])
def get_song_album(index_album,index_musica):
  try:
    find, _ = helpers.id_on_db(index_album,"albuns")
    if (not find):
      response = "Album not on DB."
    else:
      find, row = helpers.id_on_db(index_musica,"songs")
      if (find):
        response = {
          'idSong' : row[0],
          'nameSong': row[1],
          'genre': row[2],
          'explicit':row[3],
          'idSongItunes':row[4],
          'nameArtistSong':row[5],
          'nameAlbumSong':row[6],
          'idAlbumSong':row[7]
        }
      else:
        response = "Song not on DB."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)

@app.route('/albuns/<int:index>',methods=['DELETE'])
def delete_album(index):
  try:
    connection = connect_to_db()
    find, _= helpers.id_on_db(index,"albuns")
    if (not find):
      response = "Album not on DB."
    else:
      sql = "DELETE FROM albuns WHERE idAlbum=%s"
      if (connection.is_connected()):
        cursor = connection.cursor()
        cursor.execute(sql,(index,))
        connection.commit()
        response = "Deletion successful."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/musicas/<int:index>',methods=['DELETE'])
def delete_song(index):
  try:
    connection = connect_to_db()
    find, _= helpers.id_on_db(index,"songs")
    if (not find):
      response = "Song not on DB."
    else:
      sql = "DELETE FROM songs WHERE idSong=%s"
      if (connection.is_connected()):
        cursor = connection.cursor()
        cursor.execute(sql,(index,))
        connection.commit()
        response = "Deletion successful."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()
      
@app.route('/albuns/<int:index_album>/musicas/<int:index_musica>',methods=['DELETE'])
def delete_song_album(index_album,index_musica):
  try:
    find,_ = helpers.id_on_db(index_album,"albuns")
    if (not find):
      response = "Album not on DB."
    else:
      find,_ = helpers.id_on_db(index_musica,"songs")
      if(not find):
        response = "Song not on DB."
      else:
        connection = connect_to_db()
        if (connection.is_connected()):
          sql = "DELETE FROM songs WHERE idSong=%s"
          cursor = connection.cursor()
          cursor.execute(sql,(index_musica,))
          connection.commit()
          response = "Deletion successful."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index>/musicas',methods=['DELETE'])
def delete_songs_album(index):
  try:
    find,_ = helpers.id_on_db(index,"albuns")
    if (not find):
      response = "Album not on DB."
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
    print("Error: ", e)
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index>/albuns',methods=['POST'])
def add_album(index):
  try:
    newAlbum = request.get_json()
    if (not newAlbum):
      response = "No Body in request."
    else:
      findArtist, row = helpers.id_on_db(index,"artists")
      if (not findArtist):
        response = "Artist not on DB."
      else:
        connection = connect_to_db()
        if (connection.is_connected()):
          cursor = connection.cursor()
          artistId = row[2]
          if (not artistId):
            response = "Artist not on iTunes, no Albuns."
          else:
            albuns = helpers.get_type_from_id(artistId, "album")
            if (type(albuns) == str):
              response = albuns
            else:
              dataToSave = []
              for album in albuns:
                if (album['collectionName'].lower() == newAlbum['name'].lower()):
                  dataToSave.append({
                      'nameAlbum' : album['collectionName'],
                      'trackCount' : album['trackCount'],
                      'explicit' : album['collectionExplicitness'],
                      'genre' : album['primaryGenreName'],
                      'idAlbumItunes' : album['collectionId'],
                      'nameArtistAlbum' : album['artistName'],
                      'artistIdItunes' : album['artistId']
                  }) 
                  break
              if (not dataToSave):
                response = "Album not on iTunes."
              else:
                findAlbum = helpers.on_db(dataToSave[0]['idAlbumItunes'],"albuns")
                if (findAlbum):
                  response = "Album already on DB."
                else:
                  sql = "INSERT INTO albuns (nameAlbum, trackCount,explicit,genre,idAlbumItunes, nameArtistAlbum, idArtistAlbum) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                  data = (dataToSave[0]['nameAlbum'],dataToSave[0]['trackCount'],dataToSave[0]['explicit'],dataToSave[0]['genre'],dataToSave[0]['idAlbumItunes'],dataToSave[0]['nameArtistAlbum'],index)
                  cursor.execute(sql,data)
                  connection.commit()
                  response = "Added successful."
    response = jsonify(response)     
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (newAlbum and findArtist and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index>/musicas',methods=['POST'])
def add_song(index):
  try:
    newSong = request.get_json()
    findAlbum, row = helpers.id_on_db(index,"albuns")
    if (not findAlbum):
      response = "Album not on DB."
    else:
      connection = connect_to_db()
      if (connection.is_connected()):
        cursor = connection.cursor()
        albumId = row[5]
        if (not albumId):
          response = "Album not on iTunes, no Songs."
        else:
          songs = helpers.get_type_from_id(albumId,"song")
          if (type(songs) == str):
            response = songs
          else:
            dataToSave = []
            for song in songs:
              if (song['trackName'].lower() == newSong['name'].lower()):
                dataToSave.append({
                    'nameSong' : song['trackName'],
                    'explicit' : song['trackExplicitness'],
                    'genre' : song['primaryGenreName'],
                    'idSongItunes' : song['trackId'],
                    'nameArtistSong' : song['artistName'],
                    'nameAlbumSong' : song['collectionName'],
                    'artistIdItunes' : song['artistId']
                }) 
                break
            if (not dataToSave):
              response = "Song not on iTunes."
            else:
              findSong = helpers.on_db(dataToSave[0]['idSongItunes'],"songs")
              if (findSong):
                response = "Song already on DB."
              else:
                sql = "INSERT INTO songs (nameSong, explicit, genre, idSongItunes, nameArtistSong, nameAlbumSong, idAlbumSong) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                data = (dataToSave[0]['nameSong'],dataToSave[0]['genre'],dataToSave[0]['explicit'],dataToSave[0]['idSongItunes'],dataToSave[0]['nameArtistSong'],dataToSave[0]['nameAlbumSong'],index)
                cursor.execute(sql,data)
                connection.commit()
                response = "Added successful."
    response = jsonify(response)     
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (findAlbum and connection.is_connected()):
      cursor.close()
      connection.close()

# Rotas iTunes
@app.route('/artistas/<int:index>/albuns/itunes',methods=['GET'])
def get_all_albuns_artist_itunes(index):
  try:    
    find, row = helpers.id_on_db(index,"artists")
    if (not find):
      response = "Artist not on DB."
    else:  
      artistId = row[2]
      if (artistId):
        albuns = helpers.get_type_from_id(artistId, "album")
        if (type(albuns) == str):
          response = albuns
        else:
          response = []
          for album in albuns:
            response.append(
              {
                'nameArtistAlbum' : album['artistName'],
                'nameAlbum' : album['collectionName'],
                'trackCount' : album['trackCount'],
                'explicit' : album['collectionExplicitness'],
                'genre' : album['primaryGenreName'],
                'idAlbumItunes' : album['collectionId']
              }
            )
      else:
        response = "Artist not on iTunes."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)

@app.route('/artistas/<int:index>/musicas/itunes', methods=['GET'])
def get_all_songs_artist_itunes(index):
  try:
    find, row = helpers.id_on_db(index,"artists")
    if (not find):
      response = "Artist not on DB."
    else:  
      artistId = row[2]
      if (artistId):
        songs = helpers.get_type_from_id(artistId, "song")
        if (type(songs) == str):
          response = songs
        else:
          response = []
          for song in songs:
            response.append(
              {
                'nameArtistSong' : song['artistName'],
                'nameAlbumSong' : song['collectionName'],
                'nameSong' : song['trackName'],
                'explicit' : song['trackExplicitness'],
                'genre' : song['primaryGenreName'],
                'idSongItunes' : song['trackId']
              }
            )
      else:
        response = "Artist not on iTunes."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)

@app.route('/albuns/<int:index>/musicas/itunes', methods=['GET'])
def get_all_songs_album_itunes(index):
  try:
    find, row = helpers.id_on_db(index,"albuns")
    if (not find):
      response = "Album not on DB."
    else:  
      albumId = row[5]
      if (albumId):
        songs = helpers.get_type_from_id(albumId, "song")
        if (type(songs) == str):
          response = songs
        else:
          response = []
          for song in songs:
            response.append(
              {
                'nameArtistSong' : song['artistName'],
                'nameAlbumSong' : song['collectionName'],
                'nameSong' : song['trackName'],
                'explicit' : song['trackExplicitness'],
                'genre' : song['primaryGenreName'],
                'idSongItunes' : song['trackId']
              }
            )
      else:
        response = "Album not on iTunes."
    response = jsonify(response)
    response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)

if __name__ == '__main__':
  app.run(debug=True,host = '0.0.0.0')
