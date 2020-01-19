import mysql.connector
import os

def connect_to_db():  
  try:
    user = 'root'
    password = os.getenv('MYSQL_ROOT_PASSWORD')
    db = os.getenv('MYSQL_DATABASE')
    host = os.getenv('MYSQL_HOSTNAME')
    connection = mysql.connector.connect(host=host, database=db, user=user, password=password)
    if (connection.is_connected()):
      return connection
  except Exception as e:
    return "Error when connecting: " + str(e)
  