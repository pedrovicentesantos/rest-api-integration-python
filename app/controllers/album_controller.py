from helpers.format_data import format_album
from helpers.responses import bad_request, not_found, ok, internal_server_error
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
            db_album = self.repository.get_album_by_artist_by_name(name, artist)
            if (db_album):
                return bad_request('Album already exists')

            itunes_controller = ItunesController()
            album = itunes_controller.get_album_by_artist_by_name(name, artist)
            if (not album):
                return not_found('Album not found')

            self.repository.add_album(album)
            return ok(album)

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