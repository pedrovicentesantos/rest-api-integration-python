import requests

class ItunesController:
    def __init__(self):
        self. base_url = "https://itunes.apple.com/search?entity=musicArtist&term="

    def get_artist_by_name(self, name):
        try:
            url = self.base_url + name
            response = requests.get(url)
            if (response.status_code == 200):
                data = response.json()
                for artist in data['results']:
                    if (artist['artistName'].lower() == name):
                        return artist

        except Exception as e:
            print(e)