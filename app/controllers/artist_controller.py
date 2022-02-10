from helpers.format_data import format_artist
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

            self.repository.add_artist(artist)
            return ok(artist)

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