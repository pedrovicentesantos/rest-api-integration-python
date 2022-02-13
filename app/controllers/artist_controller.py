from helpers.format_data import format_artist, format_album, format_song
from helpers.responses import bad_request, not_found, ok, internal_server_error, no_content
from controllers.itunes_controller import ItunesController

class ArtistController:
    def __init__(self, repository):
        self.repository = repository

    def add_artist(self, request):
        try:
            request_data = request.get_json()
            if (not request_data):
                return bad_request('No body provided')
            if ('name' not in request_data.keys() or not request_data['name']):
                return bad_request('No name provided')
            
            artist_name = request_data['name'].lower()
            db_artist = self.repository.get_artist_by_name(artist_name)
            if (db_artist):
                return bad_request('Artist already exists')

            itunes_controller = ItunesController()
            artist = itunes_controller.get_artist_by_name(artist_name)
            if (not artist):
                return not_found('Artist not found')

            created_artist = self.repository.add_artist(artist)
            return ok(format_artist(created_artist))

        except Exception as e:
            return internal_server_error(str(e))

    def add_album_to_artist(self, index, request):
        try:
            request_data = request.get_json()
            if (not request_data):
                return bad_request('No body provided')
            if ('name' not in request_data.keys() or not request_data['name']):
                return bad_request('No name provided')
            
            artist = self.repository.get_artist_by_id(index)
            if (not artist):
                return not_found('Artist not found')
            
            album_name = request_data['name'].lower()
            album = self.repository.get_album_by_artist_id(album_name, index)
            if (album):
                return bad_request('Album already exists')

            itunes_controller = ItunesController()
            album = itunes_controller.get_album_by_artist_id(index, album_name)
            if (not album):
                return not_found('Album not found')

            created_album = self.repository.add_album(album)
            return ok(format_album(created_album))

        except Exception as e:
            return internal_server_error(str(e))

    def add_song_to_artist(self, index, request):
        try:
            request_data = request.get_json()
            if (not request_data):
                return bad_request('No body provided')
            if ('name' not in request_data.keys() or not request_data['name']):
                return bad_request('No name provided')
            
            artist = self.repository.get_artist_by_id(index)
            if (not artist):
                return not_found('Artist not found')
            
            song_name = request_data['name'].lower()
            song = self.repository.get_song_by_artist_id(song_name, index)
            if (song):
                return bad_request('Song already exists')

            itunes_controller = ItunesController()
            song = itunes_controller.get_song_by_data_id(index, song_name)
            if (not song):
                return not_found('Song not found')

            created_song = self.repository.add_song(song)
            return ok(format_song(created_song))

        except Exception as e:
            return internal_server_error(str(e))

    def get_artists(self, request):
        try:
            request_data = request.args
            query_name = None
            query_genre = None
            if ('name' in request_data.keys()):
                query_name = request_data['name'].lower()
            if ('genre' in request_data.keys()):
                query_genre = request_data['genre'].lower()

            artists = self.repository.get_artists(query_name, query_genre)
            formatted_artists = [format_artist(artist) for artist in artists]
            return ok(formatted_artists)

        except Exception as e:
            return internal_server_error(str(e))

    def delete_artist(self, index):
        try:
            deleted = self.repository.delete_artist(index)
            if (not deleted):
                return not_found('Artist not found')
            return no_content()

        except Exception as e:
            return internal_server_error(str(e))

    def update_artist(self, index, request):
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

            updated_artist = self.repository.update_artist(index, new_name, new_genre)
            if (not updated_artist):
                return not_found('Artist not found')
            return ok(format_artist(updated_artist))

        except Exception as e:
            return internal_server_error(str(e))

    def get_artist(self, index):
        try:
            artist = self.repository.get_artist_by_id(index)
            if (not artist):
                return not_found('Artist not found')
            return ok(format_artist(artist))

        except Exception as e:
            return internal_server_error(str(e))

    def get_albums(self, index, request):
        try:
            request_data = request.args
            query_name = None
            if ('name' in request_data.keys()):
                query_name = request_data['name'].lower()

            albums = self.repository.get_artist_albums(index, query_name)
            if (albums == False):
                return not_found('Artist not found')
            formatted_albums = [format_album(album) for album in albums]
            return ok(formatted_albums)

        except Exception as e:
            return internal_server_error(str(e))

    def get_songs(self, index, request):
        try:
            request_data = request.args
            query_name = None
            if ('name' in request_data.keys()):
                query_name = request_data['name'].lower()

            songs = self.repository.get_artist_songs(index, query_name)
            if (songs == False):
                return not_found('Artist not found')
            formatted_songs = [format_song(song) for song in songs]
            return ok(formatted_songs)

        except Exception as e:
            return internal_server_error(str(e))