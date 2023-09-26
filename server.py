from flask import (Flask, render_template, request, session, redirect)
from jinja2 import StrictUndefined
from model import db, connect_to_db, User, Group, UserGroup, Task, Comment
from datetime import datetime
from sqlalchemy import and_
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.context_processor
def user_info():
    if 'username' in session and session['username']:
        username = session['username']
        user = User.query.filter_by(username=username).first()

        return user.as_dict()

    else:
        session['username'] = 'user1'
        default_user = User.query.filter_by(username='user1').first()

        return default_user.as_dict()



@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/users', methods=['POST'])
def create_user():
    username = request.form.get('new-username')
    name = request.form.get('new-name')
    password = request.form.get('new-password')

    existing_username = User.query.filter_by(username=username).first()
    
    if existing_username:
        return {'success': False, 'message': 'Username unavailable'}

    user = crud.create_user(username, password, name)
    db.session.add(user)
    db.session.commit()

    session['username'] = username

    return {'success': True, 'message': 'User successfully created', 'user': user.as_dict()}


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username, password, 'username password here')

    user = User.query.filter_by(username=username).first()
    
    if not user:
        return {'success': False, 'message': 'Username not found'}
    
    if user.check_password(password):
        session['username'] = username
        return {'success': True, 'user': user.as_dict()}
    
    return {'success': False, 'message': 'Incorrect password'}


@app.route('/create-group', methods=['POST'])
def create_group():
    """creates a new group and assigns the user to it"""
    username = session['username']
    user = User.query.filter_by(username=username).first()
    admin = user.user_id

    name = request.form.get('new-group-name')
    private = request.form.get('private')
    if private == 'true':
        private = True
    elif private == 'false':
        private = False

    existing_group = Group.query.filter_by(name=name).first()
    if existing_group:
        return {'success': False, 'message': 'That group name is taken'}

    group = crud.create_group(name=name, private=private, admin=admin)
    db.session.add(group)
    db.session.commit()

    group_in_db = Group.query.filter_by(name=name).first()
    user_group = crud.create_user_group(user_id=user.user_id, group_id=group_in_db.group_id)

    db.session.add(user_group)
    db.session.commit()

    return {'success': True, 'message': f'Group {name} created', 'data': { 'group': group.as_dict() } }


@app.route('/join-group', methods=['POST'])
def join_group():
    name = request.form.get('group-name')
    print(name, 'name')
    
    username = session['username']
    user = User.query.filter_by(username=username).first()

    group = Group.query.filter_by(name=name).first()
    print(name, user, group, 'line 87')
    
    if not group:
        print('if not group')
        return {'success': False, 'message': 'Group not found'}
    
    existing_user_group = UserGroup.query.filter_by(user_id=user.user_id, group_id=group.group_id).first()
    print(existing_user_group, 'existing_user_group')
    if existing_user_group:
        return {'success': False, 'message': f"You are already in group '{name}'"}

    new_request = crud.create_request(user_id=user.user_id, group_id=group.group_id)
    db.session.add(new_request)
    db.session.commit()

    return {'success': True, 'message': f'request sent to join group {name}'}


@app.route('/current-group/<group_id>')
def current_group(group_id):
    print('in /current-group/<group_id>')
    current_group = Group.query.filter_by(group_id=group_id).first()
    session['group'] = current_group.as_dict()

    group_members = db.session.query(User)\
        .join(UserGroup)\
        .filter(UserGroup.group_id==group_id)\
        .all()

    print(group_members, 'group_members')

    tasks = Task.query.filter_by(group_id=group_id).all()

    return [task.as_dict() for task in tasks]
    


# @app.route('/tasks', methods=['GET'])
# def group_tasks():



@app.route('/tasks', methods=['POST'])
def create_task():
    current_user = user_info()
    assigned_to = request.form.get('assigned-to')
    assigned_to_user = User.query.filter_by(username=assigned_to).first()
    print(assigned_to_user, 'assigned_to_user')
    group_id = None
    if 'group' in session and session['group']:
        group_id = session['group']['group_id']
    content = request.form.get('task-content')
    urgency = int(request.form.get('task-urgency'))

    new_task = crud.create_task(assigned_by=current_user['user_id'], assigned_to=assigned_to_user.user_id, 
                     group_id=group_id, content=content, score=None, urgency=urgency, completed=False)
    
    db.session.add(new_task)
    db.session.commit()

    return {'success': True, 'message': 'Task added', 'new_task': new_task.as_dict()}


@app.route('/groups', methods=['GET'])
def user_groups():
    current_user = user_info()
    group_ids = UserGroup.query.filter_by(user_id=current_user['user_id']).all()
    group_ids = [group.group_id for group in group_ids]
    # print(group_ids)

    cur_user_groups = db.session.query(Group).filter(Group.group_id.in_(group_ids)).all()

# return cur_user_groups.map(x => x.as_dict())
    groups = []
    for group in cur_user_groups:
        groups.append(group.as_dict())
    # print(groups)

    # return groups
    return { 'success': True, 'message': f'OK', 'status': 200, 'data': { 'groups': groups } }




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
