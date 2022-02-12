from app import app
from flask import request
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

@app.route('/artists/<int:index>/songs', methods=['GET'])
def get_artist_songs(index):
  controller = ArtistController(repository)
  response = controller.get_songs(index, request)
  return response

@app.route('/artists/<int:index>/albums', methods=['POST'])
def add_album_to_artist(index):
  controller = ArtistController(repository)
  response = controller.add_album_to_artist(index, request)
  return response

@app.route('/artists/<int:index>/songs', methods=['POST'])
def add_song_to_artist(index):
  controller = ArtistController(repository)
  response = controller.add_song_to_artist(index, request)
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

@app.route('/albums/<int:index>/songs', methods=['GET'])
def get_album_songs(index):
  controller = AlbumController(repository)
  response = controller.get_songs(index, request)
  return response

@app.route('/albums/<int:index>/songs', methods=['POST'])
def add_song_to_album(index):
  controller = AlbumController(repository)
  response = controller.add_song_to_album(index, request)
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

if __name__ == '__main__':
  app.run(debug=True,host = '0.0.0.0')
