import os
from crud import create_user, create_group, create_user_group
from model import db, connect_to_db
import server


os.system('dropdb collab-todo')
os.system('createdb collab-todo')

connect_to_db(server.app)
with server.app.app_context():
    db.create_all()

    users = [
        create_user('user1', 'password', 'Bort'),
        create_user('user2', 'password', 'Bort Jr.'),
        create_user('user3', 'password', 'Kelsie'),
        create_user('user4', 'password', 'Kelsie Two'),
    ]

    db.session.add_all(users)
    db.session.commit()

    groups = [
        create_group('group1', True, 1)
    ]

    db.session.add_all(groups)
    db.session.commit()

    user_groups = [
        create_user_group(1, 1),
        create_user_group(2, 1)
    ]

    db.session.add_all(user_groups)
    db.session.commit()
    
    