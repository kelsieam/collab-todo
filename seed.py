import os
import crud
from model import db, connect_to_db
import server


os.system('dropdb collab-todo')
os.system('createdb collab-todo')

connect_to_db(server.app)
with server.app.app_context():
    db.create_all()

    users = [
        crud.create_user('user1', 'password', 'Bort'),
        crud.create_user('user2', 'password', 'Bort Jr.'),
        crud.create_user('user3', 'password', 'Kelsie'),
        crud.create_user('user4', 'password', 'Kelsie Two'),
    ]

    db.session.add_all(users)
    db.session.commit()

    groups = [
        crud.create_group('group1', True, 1),
        crud.create_group('group2', True, 2)
    ]

    db.session.add_all(groups)
    db.session.commit()

    user_groups = [
        crud.create_user_group(1, 1),
        crud.create_user_group(2, 1),
        crud.create_user_group(2, 2),
        crud.create_user_group(3, 2),
        crud.create_user_group(4, 2)
    ]

    db.session.add_all(user_groups)
    db.session.commit()
    
    tasks = [
        # assigned_by, assigned_to, group_id, content, score, urgency, completed
        crud.create_task(2, 3, 2, "ooh a task assigned to someone else", None, 5, True),
        crud.create_task(2, 4, 2, "look task assigned to someone else", None, 3, False),
        crud.create_task(2, 2, 2, "ooh a task assigned to myself", None, 2, False)
    ]

    db.session.add_all(tasks)
    db.session.commit()
    