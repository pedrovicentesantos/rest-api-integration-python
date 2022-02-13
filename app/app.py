from flask import Flask, request
from flask_cors import CORS
from flasgger import Swagger, swag_from
from controllers.artist_controller import ArtistController
from controllers.album_controller import AlbumController
from controllers.song_controller import SongController
from repositories.sqlite_repository import SQLiteRepository
from repositories.mysql_repository import MySQLRepository

def create_app(config):
    if (config == 'test'):
        repository = SQLiteRepository('initSqlite3.sql')
    else:
        repository = MySQLRepository()
    
    app = Flask(__name__)
    CORS(app)
    Swagger(app, template_file='docs/definitions.yml')

    # Artist routes
    @app.route('/artists', methods=['POST'])
    @swag_from('docs/artists/add.yml')
    def add_artist():
        controller = ArtistController(repository)
        response = controller.add_artist(request)
        return response

    @app.route('/artists', methods=['GET'])
    @swag_from('docs/artists/artists.yml')
    def get_artists():
        controller = ArtistController(repository)
        response = controller.get_artists(request)
        return response

    @app.route('/artists/<int:index>', methods=['GET'])
    @swag_from('docs/artists/artist.yml')
    def get_artist(index):
        controller = ArtistController(repository)
        response = controller.get_artist(index)
        return response

    @app.route('/artists/<int:index>', methods=['PUT'])
    @swag_from('docs/artists/update.yml')
    def update_artist(index):
        controller = ArtistController(repository)
        response = controller.update_artist(index, request)
        return response

    @app.route('/artists/<int:index>', methods=['DELETE'])
    @swag_from('docs/artists/delete.yml')
    def delete_artist(index):
        controller = ArtistController(repository)
        response = controller.delete_artist(index)
        return response

    @app.route('/artists/<int:index>/albums', methods=['GET'])
    @swag_from('docs/artists/albums.yml')
    def get_artist_albums(index):
        controller = ArtistController(repository)
        response = controller.get_albums(index, request)
        return response

    @app.route('/artists/<int:index>/songs', methods=['GET'])
    @swag_from('docs/artists/songs.yml')
    def get_artist_songs(index):
        controller = ArtistController(repository)
        response = controller.get_songs(index, request)
        return response

    @app.route('/artists/<int:index>/albums', methods=['POST'])
    @swag_from('docs/artists/add_album.yml')
    def add_album_to_artist(index):
        controller = ArtistController(repository)
        response = controller.add_album_to_artist(index, request)
        return response

    @app.route('/artists/<int:index>/songs', methods=['POST'])
    @swag_from('docs/artists/add_song.yml')
    def add_song_to_artist(index):
        controller = ArtistController(repository)
        response = controller.add_song_to_artist(index, request)
        return response

    # Album routes
    @app.route('/albums', methods=['POST'])
    @swag_from('docs/albums/add.yml')
    def add_album():
        controller = AlbumController(repository)
        response = controller.add_album(request)
        return response

    @app.route('/albums', methods=['GET'])
    @swag_from('docs/albums/albums.yml')
    def get_albums():
        controller = AlbumController(repository)
        response = controller.get_albums(request)
        return response

    @app.route('/albums/<int:index>', methods=['GET'])
    @swag_from('docs/albums/album.yml')
    def get_album(index):
        controller = AlbumController(repository)
        response = controller.get_album(index)
        return response

    @app.route('/albums/<int:index>', methods=['PUT'])
    @swag_from('docs/albums/update.yml')
    def update_album(index):
        controller = AlbumController(repository)
        response = controller.update_album(index, request)
        return response

    @app.route('/albums/<int:index>', methods=['DELETE'])
    @swag_from('docs/albums/delete.yml')
    def delete_album(index):
        controller = AlbumController(repository)
        response = controller.delete_album(index)
        return response

    @app.route('/albums/<int:index>/songs', methods=['GET'])
    @swag_from('docs/albums/songs.yml')
    def get_album_songs(index):
        controller = AlbumController(repository)
        response = controller.get_songs(index, request)
        return response

    @app.route('/albums/<int:index>/songs', methods=['POST'])
    @swag_from('docs/albums/add_song.yml')
    def add_song_to_album(index):
        controller = AlbumController(repository)
        response = controller.add_song_to_album(index, request)
        return response

    # Songs routes
    @app.route('/songs', methods=['POST'])
    @swag_from('docs/songs/add.yml')
    def add_song():
        controller = SongController(repository)
        response = controller.add_song(request)
        return response

    @app.route('/songs', methods=['GET'])
    @swag_from('docs/songs/songs.yml')
    def get_songs():
        controller = SongController(repository)
        response = controller.get_songs(request)
        return response

    @app.route('/songs/<int:index>', methods=['GET'])
    @swag_from('docs/songs/song.yml')
    def get_song(index):
        controller = SongController(repository)
        response = controller.get_song(index)
        return response

    @app.route('/songs/<int:index>', methods=['PUT'])
    @swag_from('docs/songs/update.yml')
    def update_song(index):
        controller = SongController(repository)
        response = controller.update_song(index, request)
        return response

    @app.route('/songs/<int:index>', methods=['DELETE'])
    @swag_from('docs/songs/delete.yml')
    def delete_song(index):
        controller = SongController(repository)
        response = controller.delete_song(index)
        return response

    return app