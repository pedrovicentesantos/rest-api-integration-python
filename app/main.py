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
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response 
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
        response = jsonify(response)
        response.status_code = 404
      else:
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        response.append(dict(zip(row_headers,row)))
        response = jsonify(response)
        response.status_code = 200
      return response
  except Exception as e:
    response = jsonify("Error: ", e)
    response.status_code = 400
    return response
  finally:
    if (connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas/<int:index>', methods=['PUT'])
def update_artist(index):
  try:
    artist = request.get_json()
    noParamName = False
    if (not artist):
      response = jsonify("No Body in request.")
      response.status_code = 400
    elif ("name" not in artist.keys()):
      noParamName = True
      response = jsonify("No name parameter in request body.")
      response.status_code = 400
    else:
      find, _ = helpers.id_on_db(index,"artists")
      if (not find):
        response = jsonify("Artist not on DB.")
        response.status_code = 404
      else:
        result = helpers.is_on_itunes(artist['name'])
        if (type(result) == str):
          response = jsonify(result)
          response.status_code = 400
        else:
          connection = connect_to_db()
          if (connection.is_connected()):
            # Deletar todos os albuns e musicas do artista antes
            cursor = connection.cursor()
            sql = "DELETE FROM albuns WHERE idArtistAlbum=%s"
            cursor.execute(sql,(index,))
            if (not result[0]):
              # Sem ID iTunes
              id = None
              name = artist['name']
            else:
              # Com ID iTunes
              id = result[1]
              name = result[2]
              # Colocar albuns no BD
              helpers.add_all_items_to_db(id,index,"album",cursor)
              # Pegar IDs albuns do artista
              sql = "SELECT idAlbum,idAlbumItunes FROM albuns WHERE idArtistAlbum=%s"
              cursor.execute(sql,(index,))
              rows = cursor.fetchall()
              # app.logger(rows)
              # Colocar musicas nos albuns
              for row in rows:
                helpers.add_all_items_to_db(row[1],row[0],"song",cursor)
            findNameArtist = helpers.on_db(artist,"artists")
            if (not findNameArtist):
              sql = "UPDATE artists SET nameArtist = %s, idArtistItunes=%s WHERE idArtist= %s"
              data = (name,id,index)
              cursor.execute(sql,data)
              connection.commit()
              response = jsonify("Update successful.")  
              response.status_code = 200
            else:
              response = jsonify("Artist already on DB.")  
              response.status_code = 200
    return response
  except Exception as e:
    print("Error: ", e)
  finally:
    if (artist and not noParamName and find and type(result) != str and connection.is_connected()):
      cursor.close()
      connection.close()
  
@app.route('/artistas/<int:index>', methods=['DELETE'])
def delete_artist(index):
  try:
    find, _ = helpers.id_on_db(index,"artists")
    if (not find):
      response = jsonify("Artist not on DB.")
      response.status_code = 404
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
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas', methods=['POST'])
def add_artist():
  try:
    artist = request.get_json()
    noParamName = False
    notStr = False
    if (not artist):
      response = jsonify("No Body in request.")
      response.status_code = 400
    elif ("name" not in artist.keys()):
      noParamName = True
      response = jsonify("No name parameter in request body.")
      response.status_code = 400
    elif (type(artist['name']) != str):
      notStr = True
      response = jsonify("Name parameter must be str type.")
      response.status_code = 400
    else:
      connection = connect_to_db()
      cursor = connection.cursor()
      find = helpers.on_db(artist,"artists")
      if (find):
        response = jsonify("Artist already on DB.")
        response.status_code = 200
      else:
        result = helpers.is_on_itunes(artist['name'])
        if (type(result) == str):
          response = jsonify(result)
          response.status_code = 400
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
            if (id):
              # Pegar ID do artista
              sql = "SELECT idArtist FROM artists WHERE nameArtist=%s"
              data = (name,)
              cursor = connection.cursor(pymysql.cursors.DictCursor)
              cursor.execute(sql,data)
              row = cursor.fetchone()
              # Colocar albuns no BD
              helpers.add_all_items_to_db(id,row[0],"album",cursor)
              
              # Pegar IDs albuns do artista
              sql = "SELECT idAlbum,idAlbumItunes FROM albuns WHERE idArtistAlbum=%s"
              data = (row[0],)
              cursor.execute(sql,data)
              rows = cursor.fetchall()
              # Colocar musicas nos albuns
              for row in rows:
                helpers.add_all_items_to_db(row[1],row[0],"song",cursor)
                # app.logger.info(aux)
              
            response = jsonify("Added successful.")
            response.status_code = 200
            # Commit só depois que adicionar artista, checar e adicionar albuns e checar e adicionar musicas
            connection.commit()
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (artist and not notStr and not noParamName and connection.is_connected()):
      cursor.close()
      connection.close()

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
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
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
        response = jsonify("Album not on DB.")
        response.status_code = 404
      else:
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        response.append(dict(zip(row_headers,row)))
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
        response = jsonify("Song not on DB.")
        response.status_code = 404
      else:
        row_headers = [column_name[0] for column_name in cursor.description]
        response = []
        response.append(dict(zip(row_headers,row)))
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

@app.route('/albuns/<int:index>',methods=['DELETE'])
def delete_album(index):
  try:
    connection = connect_to_db()
    find, _= helpers.id_on_db(index,"albuns")
    if (not find):
      response = jsonify("Album not on DB.")
      response.status_code = 404
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
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
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
      response = jsonify("Song not on DB.")
      response.status_code = 404
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
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (find and connection.is_connected()):
      cursor.close()
      connection.close()
      
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

@app.route('/artistas/<int:index>/albuns',methods=['POST'])
def add_album(index):
  try:
    newAlbum = request.get_json()
    noParamName = False
    inputNotString = False
    if (not newAlbum):
      response = jsonify("No Body in request.")
      response.status_code = 400
    elif ("name" not in newAlbum.keys()):
      noParamName = True
      response = jsonify("No name parameter in request body.")
      response.status_code = 400
    elif (type(newAlbum["name"]) != str):
      inputNotString = True
      response = jsonify("Name parameter must be str type.")
      response.status_code = 400
    else:
      findArtist, row = helpers.id_on_db(index,"artists")
      if (not findArtist):
        response = jsonify("Artist not on DB.")
        response.status_code = 404
      else:
        connection = connect_to_db()
        if (connection.is_connected()):
          cursor = connection.cursor()
          artistId = row[2]
          if (not artistId):
            response = jsonify("Artist not on iTunes, no Albuns.")
            response.status_code = 200
          else:
            albuns = helpers.get_type_from_id(artistId, "album")
            if (type(albuns) == str):
              response = albuns
              response = jsonify(response)
              response.status_code = 400
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
                response = jsonify("Album not on iTunes.")
                response.status_code = 200
              else:
                findAlbum = helpers.on_db(dataToSave[0]['idAlbumItunes'],"albuns")
                if (findAlbum):
                  response = jsonify("Album already on DB.")
                  response.status_code = 200
                else:
                  sql = "INSERT INTO albuns (nameAlbum, trackCount,explicit,genre,idAlbumItunes, nameArtistAlbum, idArtistAlbum) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                  data = (dataToSave[0]['nameAlbum'],dataToSave[0]['trackCount'],dataToSave[0]['explicit'],dataToSave[0]['genre'],dataToSave[0]['idAlbumItunes'],dataToSave[0]['nameArtistAlbum'],index)
                  cursor.execute(sql,data)
                  connection.commit()
                  response = jsonify("Added successful.")
                  response.status_code = 200
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (newAlbum and not noParamName and not inputNotString and findArtist and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/albuns/<int:index>/musicas',methods=['POST'])
def add_song(index):
  try:
    newSong = request.get_json()
    noParamName = False
    inputNotString = False
    if (not newSong):
      response = jsonify("No Body in request.")
      response.status_code = 400
    elif ("name" not in newSong.keys()):
      noParamName = True
      response = jsonify("No name parameter in request body.")
      response.status_code = 400
    elif (type(newSong["name"]) != str):
      inputNotString = True
      response = jsonify("Name parameter must be str type.")
      response.status_code = 400
    else:
      findAlbum, row = helpers.id_on_db(index,"albuns")
      if (not findAlbum):
        response = jsonify("Album not on DB.")
        response.status_code = 404
      else:
        connection = connect_to_db()
        if (connection.is_connected()):
          cursor = connection.cursor()
          albumId = row[5]
          if (not albumId):
            response = jsonify("Album not on iTunes, no Songs.")
            response.status_code = 200
          else:
            songs = helpers.get_type_from_id(albumId,"song")
            if (type(songs) == str):
              response = jsonify(songs)
              response.status_code = 400
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
                response = jsonify("Song not on iTunes.")
                response.status_code = 200
              else:
                findSong = helpers.on_db(dataToSave[0]['idSongItunes'],"songs")
                if (findSong):
                  response = jsonify("Song already on DB.")
                  response.status_code = 200
                else:
                  sql = "INSERT INTO songs (nameSong, explicit, genre, idSongItunes, nameArtistSong, nameAlbumSong, idAlbumSong) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                  data = (dataToSave[0]['nameSong'],dataToSave[0]['explicit'],dataToSave[0]['genre'],dataToSave[0]['idSongItunes'],dataToSave[0]['nameArtistSong'],dataToSave[0]['nameAlbumSong'],index)
                  cursor.execute(sql,data)
                  connection.commit()
                  response = jsonify("Added successful.")
                  response.status_code = 200              
    return response
  except Exception as e:
    response = jsonify("Error: " + str(e))
    response.status_code = 400
    return response
  finally:
    if (newSong and not noParamName and not inputNotString and findAlbum and connection.is_connected()):
      cursor.close()
      connection.close()

@app.route('/artistas', methods=['DELETE'])
def delete_all_artists():
  try:
    sql = "DELETE FROM artists"
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
