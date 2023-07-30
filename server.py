from flask import (Flask, render_template, request, session, redirect)
from jinja2 import StrictUndefined
from model import db, connect_to_db, User, Group
from datetime import datetime
from sqlalchemy import and_
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    name = request.form.get('first-name')
    username = request.form.get('username')
    password = request.form.get('password')

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


@app.route('/groups', methods=['POST'])
def create_group():
    """creates a new group and assigns the user to it"""
    name = request.form.get('new-group-name')
    password = request.form.get('new-group-password')

    group = crud.create_group(password=password, name=name)

    db.session.add(group)
    db.session.commit()


@app.route('/groups', methods=['PATCH'])
def join_group():
    name = request.form.get('group-name')
    password = request.form.get('group-password')
    
    username = session['username']
    cur_user = User.query.filter_by(username=username).first()

    group = Group.query.filter_by(name=name).first()
    
    if not group:
        return {'success': False, 'message': 'Group not found'}
    
    if group.check_password(password):
        cur_user.group_id = group.group_id
        return {'success': True, 'message': 'Added to group {name}'}
    
    return {'success': False, 'message': 'Incorrect password'}









if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
