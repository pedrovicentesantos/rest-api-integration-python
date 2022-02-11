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
                    if (album['collectionName'].lower() == name):
                        return album

        except Exception as e:
            print(e)