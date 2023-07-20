import sqlite3
from db_config import DATABASE_FILENAME, INIT_SCHEMA_FILENAME

connection = sqlite3.connect(DATABASE_FILENAME)


with open(INIT_SCHEMA_FILENAME) as f:
    connection.executescript(f.read())


connection.commit()
connection.close()