import sqlite3
from sqlite3 import Error


def get_db(database, g):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database, isolation_level=None)

    return db


def query(connection, *args):
  cursor = connection.cursor()
  try:
    if len(args) > 1:
      cursor.execute(args[0], args[1])
    else:
      cursor.execute(args[0])
    result = cursor.fetchall()
    
    connection.commit()

    return result
    
  except Error as e:
    return (e)