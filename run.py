from app import create_app
import os
from flask_sqlalchemy import event
from app.models import MuralPhoto


def after_photo_delete_listener(mapper, connection, target):
    if os.path.exists(target.full_filename):
        os.remove(target.full_filename)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

event.listen(MuralPhoto, 'after_delete', after_photo_delete_listener)

if __name__ == '__main__':
    app.run()