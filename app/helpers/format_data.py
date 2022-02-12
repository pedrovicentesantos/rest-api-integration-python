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

def format_song(song):
    return {
        'id': song[0],
        'name': song[1].capitalize(),
        'explicit': song[2],
        'genre': song[3].capitalize(),
        'artist': song[4].capitalize(),
        'artistId': song[5],
        'album': song[6].capitalize(),
        'albumId': song[7],
        'url': song[8],
        'duration': song[9],
    }