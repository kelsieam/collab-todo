import os
from crud import create_user
from model import db, connect_to_db
import server


os.system('dropdb collab-todo')
os.system('createdb collab-todo')

connect_to_db(server.app)
with server.app.app_context():
    db.create_all()

    users = [
        create_user('user1', 'password', 'Bryan'),
        create_user('user2', 'password', 'Cindy'),
        create_user('user3', 'password', 'Kelsie')
    ]

    db.session.add_all(users)
    db.session.commit()

    
    