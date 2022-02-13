import os
import mysql.connector
from repositories.base_repository import BaseRepository

class MySQLRepository(BaseRepository):
    def __init__(self, init_file=None):
        super().__init__(init_file)

    def connect(self):
        user = 'root'
        password = os.getenv('MYSQL_ROOT_PASSWORD')
        db = os.getenv('MYSQL_DATABASE')
        host = os.getenv('MYSQL_HOSTNAME')
        connection = mysql.connector.connect(host=host, database=db, user=user, password=password)
        if (connection.is_connected()):
            return connection

     # Artist functionalities
    def get_artist_by_id(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM artists WHERE id=%s', (id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_artist_by_name(self, name):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM artists WHERE name=%s', (name,))
        row = cursor.fetchone()
        conn.close()
        return row
  
    def add_artist(self, data):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO artists (id,name,genre) VALUES (%s,%s,%s)',
            (data['artistId'], data['artistName'].lower(), data['primaryGenreName'].lower(),)
        )
        conn.commit()
        artist = self.get_artist_by_id(data['artistId'])
        conn.close()
        return artist

    def get_artists(self, name, genre):
        conn = self.connect()
        cursor = conn.cursor()
        if (name and genre):
            cursor.execute('SELECT * FROM artists WHERE name LIKE %s AND genre=%s', ('%{}%'.format(name), genre,))
        elif (name):
            cursor.execute('SELECT * FROM artists WHERE name LIKE %s', ('%{}%'.format(name),))
        elif (genre):
            cursor.execute('SELECT * FROM artists WHERE genre=%s', (genre,))
        else:
            cursor.execute('SELECT * FROM artists')

        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_artist(self, id, name, genre):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_artist_by_id(id)):
            if (name):
                cursor.execute('UPDATE artists SET name=%s WHERE id=%s', (name, id,))
            if (genre):
                cursor.execute('UPDATE artists SET genre=%s WHERE id=%s', (genre, id,))
            conn.commit()
            artist = self.get_artist_by_id(id)
            conn.close()
            return artist
        return False

    def delete_artist(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_artist_by_id(id)):
            cursor.execute('DELETE FROM artists WHERE id=%s', (id,))
            conn.commit()
            conn.close()
            return True
        return False

    def get_artist_albums(self, id, name):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_artist_by_id(id)):
            if (name):
                cursor.execute('SELECT * FROM albums WHERE artistId=%s AND name LIKE %s', (id, '%{}%'.format(name),))
            else:
                cursor.execute('SELECT * FROM albums WHERE artistId=%s', (id,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        return False

    def get_artist_songs(self, id, name):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_artist_by_id(id)):
            if (name):
                cursor.execute('SELECT * FROM songs WHERE artistId=%s AND name LIKE %s', (id, '%{}%'.format(name),))
            else:
                cursor.execute('SELECT * FROM songs WHERE artistId=%s', (id,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        return False

    # Album functionalities
    def get_album_by_id(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM albums WHERE id=%s', (id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_album_by_artist_name(self, name, artist):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM albums WHERE name=%s AND artistName=%s', (name, artist,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_album_by_artist_id(self, name, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM albums WHERE name=%s AND artistId=%s', (name, id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def add_album(self, data):
        conn = self.connect()
        cursor = conn.cursor()
        date = data['releaseDate'].replace("T", " ").replace("Z", "")
        cursor.execute(
            'INSERT INTO albums (id,name,trackCount,explicit,genre,artistName,artistId,releaseDate,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (
                data['collectionId'],
                data['collectionName'].lower(),
                data['trackCount'],
                data['collectionExplicitness'],
                data['primaryGenreName'].lower(),
                data['artistName'].lower(),
                data['artistId'],
                date,
                data['collectionViewUrl'],
            )
        )
        conn.commit()
        album = self.get_album_by_id(data['collectionId'])
        conn.close()
        return album

    def get_albums(self, name, artist, genre):
        conn = self.connect()
        cursor = conn.cursor()
        if (name and artist and genre):
            cursor.execute('SELECT * FROM albums WHERE name LIKE %s AND artistName LIKE %s AND genre=%s', ('%{}%'.format(name), '%{}%'.format(artist), genre,))
        elif (name and artist):
            cursor.execute('SELECT * FROM albums WHERE name LIKE %s AND artistName LIKE %s', ('%{}%'.format(name), '%{}%'.format(artist),))
        elif (name and genre):
            cursor.execute('SELECT * FROM albums WHERE name LIKE %s AND genre=%s', ('%{}%'.format(name), genre,))
        elif (artist and genre):
            cursor.execute('SELECT * FROM albums WHERE artistName LIKE %s AND genre=%s', ('%{}%'.format(artist), genre,))
        elif (name):
            cursor.execute('SELECT * FROM albums WHERE name LIKE %s', ('%{}%'.format(name),))
        elif (artist):
            cursor.execute('SELECT * FROM albums WHERE artistName LIKE %s', ('%{}%'.format(artist),))
        elif (genre):
            cursor.execute('SELECT * FROM albums WHERE genre=%s', (genre,))
        else:
            cursor.execute('SELECT * FROM albums')

        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_album(self, id, name, genre):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_album_by_id(id)):
            if (name):
                cursor.execute('UPDATE albums SET name=%s WHERE id=%s', (name, id,))
            if (genre):
                cursor.execute('UPDATE albums SET genre=%s WHERE id=%s', (genre, id,))
            conn.commit()
            album = self.get_album_by_id(id)
            conn.close()
            return album
        return False

    def delete_album(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_album_by_id(id)):
            cursor.execute('DELETE FROM albums WHERE id=%s', (id,))
            conn.commit()
            conn.close()
            return True
        return False

    def get_album_songs(self, id, name):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_album_by_id(id)):
            if (name):
                cursor.execute('SELECT * FROM songs WHERE albumId=%s AND name LIKE %s', (id, '%{}%'.format(name),))
            else:
                cursor.execute('SELECT * FROM songs WHERE albumId=%s', (id,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        return False

    # Song functionalities
    def get_song_by_id(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE id=%s', (id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_song_by_artist_and_album_names(self, name, artist, album):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE name=%s AND artistName=%s AND albumName=%s', (name, artist, album,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def get_song_by_artist_id(self, name, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE name=%s AND artistId=%s', (name, id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_song_by_album_id(self, name, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE name=%s AND albumId=%s', (name, id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def add_song(self, data):
        conn = self.connect()
        cursor = conn.cursor()
        duration_in_minutes = data['trackTimeMillis'] / 1000 / 60
        cursor.execute(
            'INSERT INTO songs (id,name,explicit,genre,artistName,artistId,albumName,albumId,url,durationMinutes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (
                data['trackId'],
                data['trackName'].lower(),
                data['trackExplicitness'],
                data['primaryGenreName'].lower(),
                data['artistName'].lower(),
                data['artistId'],
                data['collectionName'].lower(),
                data['collectionId'],
                data['trackViewUrl'],
                duration_in_minutes,
            )
        )
        conn.commit()
        song = self.get_song_by_id(data['trackId'])
        conn.close()
        return song

    def get_songs(self, name, artist, album, genre):
        conn = self.connect()
        cursor = conn.cursor()
        query = 'SELECT * FROM songs'
        query_object = []

        if (name):
            query += ' WHERE name LIKE %s'
            query_object.append('%{}%'.format(name))
        if (artist):
            if (len(query_object) > 0):
                query += ' AND artistName LIKE %s'
            else:
                query += ' WHERE artistName LIKE %s'
            query_object.append('%{}%'.format(artist))
        if (album):
            if (len(query_object) > 0):
                query += ' AND albumName LIKE %s'
            else:
                query += ' WHERE albumName LIKE %s'
            query_object.append('%{}%'.format(album))
        if (genre):
            if (len(query_object) > 0):
                query += ' AND genre=%s'
            else:
                query += ' WHERE genre=%s'
            query_object.append(genre)
        
        cursor.execute(query, tuple(query_object,))

        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_song(self, id, name, genre):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_song_by_id(id)):
            if (name):
                cursor.execute('UPDATE songs SET name=%s WHERE id=%s', (name, id,))
            if (genre):
                cursor.execute('UPDATE songs SET genre=%s WHERE id=%s', (genre, id,))
            conn.commit()
            song = self.get_song_by_id(id)
            conn.close()
            return song
        return False

    def delete_song(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_song_by_id(id)):
            cursor.execute('DELETE FROM songs WHERE id=%s', (id,))
            conn.commit()
            conn.close()
            return True
        return False