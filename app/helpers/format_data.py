def format_artist(artist):
    return {
        'id': artist[0],
        'name': artist[1].capitalize(),
        'genre': artist[2].capitalize(),
    }