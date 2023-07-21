from dbOperations import getConnection
from db_config import INIT_SCHEMA_FILENAME

connection = getConnection()
cursor = connection.cursor()

with open(INIT_SCHEMA_FILENAME) as f:
    cursor.execute(f.read())


connection.commit()
cursor.close()
connection.close()