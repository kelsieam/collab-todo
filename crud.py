from model import connect_to_db, User, Group, UserGroup


def create_user(username, password, name):
    user = User(username=username, name=name)
    user.set_password(password)
    
    return user


def create_group(password, name):
    group = Group(name=name)
    group.set_password(password)

    return group


def create_user_group(user_id, group_id):
    user_group = UserGroup(user_id=user_id, group_id=group_id)

    return user_group


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
