# ADB1_Flask
 * Import requrements for the python project:
 ```
pip install -r requirements.txt
```
 * Configure connection to postgres in `config.py`
 ```python
POSTGRES_URL = '192.168.99.102:32768'
POSTGRES_USER = 'postgres'
POSTGRES_PW = ''
POSTGRES_DB = 'abd'
```

 * Initialize the database whith these three comments 
```
>python manage.py db init
>python manage.py db migrate
>python manage.py db upgrade
```
