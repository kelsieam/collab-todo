from flask import (Flask, render_template, request, session, redirect)
from jinja2 import StrictUndefined
from model import db, connect_to_db, User, Group, UserGroup
from datetime import datetime
from sqlalchemy import and_
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



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

    return {'success': True, 'message': 'User successfully created'}


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

    name = request.form.get('new-group-name')
    password = request.form.get('new-group-password')

    group = crud.create_group(password=password, name=name)
    db.session.add(group)
    db.session.commit()

    group_in_db = Group.query.filter_by(name=name).first()
    user_group = crud.create_user_group(user_id=user.user_id, group_id=group_in_db.group_id)

    db.session.add(user_group)
    db.session.commit()


    return {'success': True, 'message': f'Group {name} created'}


@app.route('/join-group', methods=['POST'])
def join_group():
    name = request.form.get('group-name')
    password = request.form.get('group-password')
    
    username = session['username']
    user = User.query.filter_by(username=username).first()

    group = Group.query.filter_by(name=name).first()
    print(name, password, user, group, 'line 87')
    
    if not group:
        print('if not group')
        return {'success': False, 'message': 'Group not found'}
    
    if group.check_password(password):
        print('if group.check_password')
        existing_user_group = UserGroup.query.filter_by(user_id=user.user_id, group_id=group.group_id).first()
        print(existing_user_group, 'existing_user_group')
        if existing_user_group:
            return {'success': False, 'message': f"You are already in group '{name}'"}
        
        user_group = crud.create_user_group(user_id=user.user_id, group_id=group.group_id)
        db.session.add(user_group)
        db.session.commit()

        return {'success': True, 'message': f'Added to group {name}'}

    return {'success': False, 'message': 'Incorrect password'}









if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
