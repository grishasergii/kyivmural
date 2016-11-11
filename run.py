from app import create_app, db
import os
from flask_sqlalchemy import event
from app.models import MuralPhoto
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


def after_photo_delete_listener(mapper, connection, target):
    if os.path.exists(target.full_filename):
        os.remove(target.full_filename)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(__file__), 'migrations'))

manager = Manager(app)
manager.add_command('db', MigrateCommand)

event.listen(MuralPhoto, 'after_delete', after_photo_delete_listener)

if __name__ == '__main__':
    manager.run()