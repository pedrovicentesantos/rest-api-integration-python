import sqlite3
from repositories.base_repository import BaseRepository

class SQLiteRepository(BaseRepository):
    def __init__(self, init_file):
        super().__init__(init_file)

    def connect(self):
        conn = sqlite3.connect('./music.db')
        return conn
