def format_artist(artist):
    return {
        'id': artist[0],
        'name': artist[1].capitalize(),
        'genre': artist[2].capitalize(),
    }

def format_album(album):
    return {
        'id': album[0],
        'name': album[1].capitalize(),
        'trackCount': album[2],
        'explicit': album[3],
        'genre': album[4].capitalize(),
        'artist': album[5].capitalize(),
        'artistId': album[6],
        'releaseDate': album[7],
        'url': album[8],
    }