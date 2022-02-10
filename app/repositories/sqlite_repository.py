import sqlite3
import os

class SQLiteRepository:
    def __init__(self):
        conn = self.connect()
        cursor = conn.cursor()
        path = os.path.join(os.getcwd(), 'db', 'initSqlite3.sql')
        init_sql_file = open(path, 'r')
        sql_as_string = init_sql_file.read()
        cursor.executescript(sql_as_string)
        conn.commit()
        conn.close()

    def connect(self):
        conn = sqlite3.connect('./music.db')
        return conn
    
    def add_artist(self, data):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO artists (id,name,genre) VALUES (?,?,?)',
            (data['artistId'], data['artistName'].lower(), data['primaryGenreName'].lower(),)
        )
        conn.commit()
        conn.close()
    
    def get_artist_by_name(self, name):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM artists WHERE name=?', (name,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_artist_by_id(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM artists WHERE id=?', (id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_artists(self, name, genre):
        conn = self.connect()
        cursor = conn.cursor()
        if (name and genre):
            cursor.execute('SELECT * FROM artists WHERE name LIKE ? AND genre=?', ('%{}%'.format(name), genre,))
        elif (name):
            cursor.execute('SELECT * FROM artists WHERE name LIKE ?', ('%{}%'.format(name),))
        elif (genre):
            cursor.execute('SELECT * FROM artists WHERE genre=?', (genre,))
        else:
            cursor.execute('SELECT * FROM artists')

        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete_artist(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_artist_by_id(id)):
            cursor.execute('DELETE FROM artists WHERE id=?', (id,))
            conn.commit()
            conn.close()
            return True
        return False

    def update_artist(self, id, name, genre):
        conn = self.connect()
        cursor = conn.cursor()
        if (self.get_artist_by_id(id)):
            if (name):
                cursor.execute('UPDATE artists SET name=? WHERE id=?', (name, id,))
            if (genre):
                cursor.execute('UPDATE artists SET genre=? WHERE id=?', (genre, id,))
            conn.commit()
            artist = self.get_artist_by_id(id)
            conn.close()
            return artist
        return False