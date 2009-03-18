


DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
DATABASE_OPTIONS  =  {"init_command": "SET storage_engine=INNODB"}  #database engine to use when create tables via models

SECRET_KEY = ''

#internal ip
INTERNAL_IPS = ('',)

#Site URL
SITE_URL = ""


