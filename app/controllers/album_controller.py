from helpers.format_data import format_album, format_song
from helpers.responses import bad_request, not_found, ok, internal_server_error, no_content
from controllers.itunes_controller import ItunesController

class AlbumController:
    def __init__(self, repository):
        self.repository = repository

    def add_album(self, request):
        try:
            request_data = request.get_json()
            if (not request_data):
                return bad_request('No body provided')
            if ('name' not in request_data.keys() or not request_data['name']):
                return bad_request('No name provided')
            if ('artist' not in request_data.keys() or not request_data['artist']):
                return bad_request('No artist provided')
            
            name = request_data['name'].lower()
            artist = request_data['artist'].lower()
            db_album = self.repository.get_album_by_artist_name(name, artist)
            if (db_album):
                return bad_request('Album already exists')

            itunes_controller = ItunesController()
            album = itunes_controller.get_album_by_artist_name(name, artist)
            if (not album):
                return not_found('Album not found')

            self.repository.add_album(album)
            return ok(album)

        except Exception as e:
            return internal_server_error(str(e))

    def add_song_to_album(self, index, request):
        try:
            request_data = request.get_json()
            if (not request_data):
                return bad_request('No body provided')
            if ('name' not in request_data.keys() or not request_data['name']):
                return bad_request('No name provided')
            
            album = self.repository.get_album_by_id(index)
            if (not album):
                return not_found('Album not found')
            
            song_name = request_data['name'].lower()
            song = self.repository.get_song_by_album_id(song_name, index)
            if (song):
                return bad_request('Song already exists')

            itunes_controller = ItunesController()
            song = itunes_controller.get_song_by_data_id(index, song_name)
            if (not song):
                return not_found('Song not found')

            self.repository.add_song(song)
            return ok(song)

        except Exception as e:
            return internal_server_error(str(e))

    def get_albums(self, request):
        try:
            request_data = request.args
            query_name = None
            query_genre = None
            query_artist = None
            if ('name' in request_data.keys()):
                query_name = request_data['name'].lower()
            if ('genre' in request_data.keys()):
                query_genre = request_data['genre'].lower()
            if ('artist' in request_data.keys()):
                query_artist = request_data['artist'].lower()

            albums = self.repository.get_albums(query_name, query_artist, query_genre)
            formatted_albums = [format_album(album) for album in albums]
            return ok(formatted_albums)

        except Exception as e:
            return internal_server_error(str(e))

    def update_album(self, index, request):
        try:
            request_data = request.get_json()
            if (not request_data):
                return bad_request('No body provided')
            new_name = None
            new_genre = None
            if ('name' in request.get_json().keys()):
                new_name = request.get_json()['name'].lower()
            if ('genre' in request.get_json().keys()):
                new_genre = request.get_json()['genre'].lower()

            updated_album = self.repository.update_album(index, new_name, new_genre)
            if (not updated_album):
                return not_found('Album not found')
            return ok(format_album(updated_album))

        except Exception as e:
            return internal_server_error(str(e))

    def delete_album(self, index):
        try:
            deleted = self.repository.delete_album(index)
            if (not deleted):
                return not_found('Album not found')
            return no_content()

        except Exception as e:
            return internal_server_error(str(e))

    def get_album(self, index):
        try:
            album = self.repository.get_album_by_id(index)
            if (not album):
                return not_found('Album not found')
            return ok(format_album(album))

        except Exception as e:
            return internal_server_error(str(e))

    def get_songs(self, index, request):
        try:
            request_data = request.args
            query_name = None
            if ('name' in request_data.keys()):
                query_name = request_data['name'].lower()

            songs = self.repository.get_album_songs(index, query_name)
            if (songs == False):
                return not_found('Album not found')
            formatted_songs = [format_song(song) for song in songs]
            return ok(formatted_songs)

        except Exception as e:
            return internal_server_error(str(e))
