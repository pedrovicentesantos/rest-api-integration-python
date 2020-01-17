import mysql.connector
import config

def connect_to_db():
  try:
    connection = mysql.connector.connect(host=config.host, database=config.db, user=config.user, password=config.password)
    if (connection.is_connected()):
      return connection
  except Exception as e:
    print("Error: ", e)
  