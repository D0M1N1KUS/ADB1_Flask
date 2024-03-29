from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from db import DbContainer
import tables

app = DbContainer.get_app()
db = DbContainer.get_db()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
