import os
import urllib.parse as urlparse
url = urlparse.urlparse(os.environ['DATABASE_URL'])
DATABASE_NAME = url.path[1:]
HOST = url.hostname
USER = url.username
PASSWORD = url.password
INIT_SCHEMA_FILENAME = 'schema.sql'