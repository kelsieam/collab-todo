from model import db, connect_to_db, User, Group, UserGroup, Request, Task, Comment
import random
import string


def create_user(username, password, name):
    user = User(username=username, name=name)
    user.set_password(password)
    
    return user


def create_group(name, private, admin):

    while True: # check for existing group code
        chars = string.ascii_letters + string.digits
        group_code = ''.join(random.choice(chars) for _ in range(6))
        existing_group = Group.query.filter_by(group_code=group_code).first()
        if not existing_group:
            break
    
    group = Group(name=name, private=private, admin=admin, group_code=group_code)

    return group


def create_user_group(user_id, group_id):
    user_group = UserGroup(user_id=user_id, group_id=group_id)

    return user_group


def create_request(user_id, group_id):
    request = Request(user_id=user_id, group_id=group_id)

    return request


def create_task(assigned_by, assigned_to, group_id, content, score, urgency, completed):
    task = Task(assigned_by=assigned_by, assigned_to=assigned_to, group_id=group_id,
                content=content, score=score, urgency=urgency, completed=completed)

    return task


def create_comment(task_id, user_id, content):
    comment = Comment(task_id=task_id, user_id=user_id, content=content)

    return comment



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
