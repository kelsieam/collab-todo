from model import connect_to_db, User, Group, UserGroup, Request, Task, Comment


def create_user(username, password, name):
    user = User(username=username, name=name)
    user.set_password(password)
    
    return user


def create_group(name, private, admin):
    group = Group(name=name, private=private, admin=admin)

    return group


def create_user_group(user_id, group_id):
    user_group = UserGroup(user_id=user_id, group_id=group_id)

    return user_group


def create_request(user_id, group_id):
    request = Request(user_id=user_id, group_id=group_id)

    return request


def create_task(assigned_by_id, assigned_to_id, group_id, content, score, urgency, completed):
    task = Task(assigned_by_id=assigned_by_id, assigned_to_id=assigned_to_id, group_id=group_id,
                content=content, score=score, urgency=urgency, completed=completed)

    return task


def create_comment(task_id, user_id, content):
    comment = Comment(task_id=task_id, user_id=user_id, content=content)

    return comment



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
