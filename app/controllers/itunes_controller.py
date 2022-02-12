import requests

class ItunesController:
    def __init__(self):
        self. base_url = "https://itunes.apple.com/search?entity"

    def get_artist_by_name(self, name):
        try:
            url = '{}=musicArtist&term={}'.format(self.base_url, name)
            response = requests.get(url)
            if (response.status_code == 200):
                data = response.json()
                for artist in data['results']:
                    if (artist['artistName'].lower() == name):
                        return artist

        except Exception as e:
            print(e)

    def get_album_by_artist_by_name(self, name, artist):
        try:
            url = '{}=album&term={}'.format(self.base_url, artist)
            response = requests.get(url)
            if (response.status_code == 200):
                data = response.json()
                for album in data['results']:
                    if (album['collectionName'].lower() == name
                        and album['artistName'].lower() == artist
                    ):
                        return album

        except Exception as e:
            print(e)

    def get_song_by_artist_and_album_by_name(self, name, artist, album):
        try:
            url = '{}=musicTrack&term={}'.format(self.base_url, album)
            response = requests.get(url)
            if (response.status_code == 200):
                data = response.json()
                for song in data['results']:
                    if (song['collectionName'].lower() == album
                        and song['artistName'].lower() == artist
                        and song['trackName'].lower() == name
                    ):
                        return song

        except Exception as e:
            print(e)