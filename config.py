# import os
#
# os.environ['DEBUG'] = "1"

POSTGRES_URL = 'localhost:32768'
POSTGRES_USER = 'postgres'
POSTGRES_PW = ''
POSTGRES_DB = 'abd'

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
