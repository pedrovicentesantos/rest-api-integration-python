from helpers.format_data import format_song
from helpers.responses import bad_request, not_found, ok, internal_server_error, no_content
from controllers.itunes_controller import ItunesController

class SongController:
    def __init__(self, repository):
        self.repository = repository

    def add_song(self, request):
        try:
            request_data = request.get_json()
            if (not request_data):
                return bad_request('No body provided')
            if ('name' not in request_data.keys() or not request_data['name']):
                return bad_request('No name provided')
            if ('artist' not in request_data.keys() or not request_data['artist']):
                return bad_request('No artist provided')
            if ('album' not in request_data.keys() or not request_data['album']):
                return bad_request('No album provided')
            
            name = request_data['name'].lower()
            artist = request_data['artist'].lower()
            album = request_data['album'].lower()
            db_song = self.repository.get_song_by_artist_and_album_by_name(name, artist, album)
            if (db_song):
                return bad_request('Song already exists')

            itunes_controller = ItunesController()
            song = itunes_controller.get_song_by_artist_and_album_by_name(name, artist, album)
            if (not song):
                return not_found('Song not found')

            self.repository.add_song(song)
            return ok(song)

        except Exception as e:
            return internal_server_error(str(e))

    def get_songs(self, request):
        try:
            request_data = request.args
            query_name = None
            query_genre = None
            query_artist = None
            query_album = None
            if ('name' in request_data.keys()):
                query_name = request_data['name'].lower()
            if ('genre' in request_data.keys()):
                query_genre = request_data['genre'].lower()
            if ('artist' in request_data.keys()):
                query_artist = request_data['artist'].lower()
            if ('album' in request_data.keys()):
                query_album = request_data['album'].lower()

            songs = self.repository.get_songs(query_name, query_artist, query_album, query_genre)
            formatted_songs = [format_song(song) for song in songs]
            return ok(formatted_songs)

        except Exception as e:
            return internal_server_error(str(e))

    def update_song(self, index, request):
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

            updated_song = self.repository.update_song(index, new_name, new_genre)
            if (not updated_song):
                return not_found('Song not found')
            return ok(format_song(updated_song))

        except Exception as e:
            return internal_server_error(str(e))

    def delete_song(self, index):
        try:
            deleted = self.repository.delete_song(index)
            if (not deleted):
                return not_found('Song not found')
            return no_content()

        except Exception as e:
            return internal_server_error(str(e))

    def get_song(self, index):
        try:
            song = self.repository.get_song_by_id(index)
            if (not song):
                return not_found('Song not found')
            return ok(format_song(song))

        except Exception as e:
            return internal_server_error(str(e))