from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """a user"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(30), nullable=False)

    user_groups = db.relationship('UserGroup', back_populates='user')
    # group = db.relationship('Group', back_populates='user')
    request = db.relationship('Request', back_populates='user')
    # task = db.relationship('Task', back_populates='user')
    comment = db.relationship('Comment', back_populates='user')
    

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'name': self.name,
        }


class UserGroup(db.Model):
    """join table for users and groups"""
    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))

    user = db.relationship('User', back_populates='user_groups')
    group = db.relationship('Group', back_populates='user_groups')

    def __repr__(self):
        return f'<UserGroup id={self.id} user_id={self.user_id} group_id={self.group_id}>'


class Group(db.Model):
    """a group of users"""
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    name = db.Column(db.String, nullable=False)
    private = db.Column(db.Boolean, nullable=False, default=True)
    admin = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    group_code = db.Column(db.String, nullable=False)

    user_groups = db.relationship('UserGroup', back_populates='group')
    # user = db.relationship('User', back_populates='group')
    request = db.relationship('Request', back_populates='group')
    task = db.relationship('Task', back_populates='group')
    # comment = db.relationship('Comment', back_populates='group')

    def __repr__(self):
        return f'<Group group_id={self.group_id} name={self.name}>'

    def as_dict(self):
        return {
            'group_id': self.group_id,
            'name': self.name,
            'private': self.private,
            'admin': self.admin
        }


class Request(db.Model):
    """requests for joining groups"""
    __tablename__ = 'requests'

    request_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))

    user = db.relationship('User', back_populates='request')
    group = db.relationship('Group', back_populates='request')

    def __repr__(self):
        return f'<Request request_id={self.request_id} user_id={self.user_id} group_id={self.group_id}>'

    def as_dict(self):
        return {
            'request_id': self.request_id,
            'user_id': self.user_id,
            'group_id': self.group_id
        }


class Task(db.Model):
    """tasks that users can assign to themselves or others"""
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer,
                        autoincrement=True, 
                        primary_key=True)
    assigned_by = db.Column(db.Integer)
    assigned_to = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
    content = db.Column(db.String,
                        nullable=False)
    score = db.Column(db.Integer, default=None)
    urgency = db.Column(db.Integer, default=None)
    completed = db.Column(db.Boolean, default=False)

    # assigned_to = db.relationship('User', foreign_keys=[assigned_to_id])
    # assigned_by = db.relationship('User', foreign_keys=[assigned_by_id])
    group = db.relationship('Group', back_populates='task')

    def __repr__(self):
        return f'<Task task_id={self.task_id} content={self.content}>'
    
    def as_dict(self):
        return {
            'task_id': self.task_id,
            'assigned_by': self.assigned_by,
            'assigned_to': self.assigned_to,
            'group_id': self.group_id,
            'content': self.content,
            'score': self.score,
            'urgency': self.urgency,
            'completed': self.completed
        }


class Comment(db.Model):
    """comments for tasks"""
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer,
                autoincrement=True, 
                primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.String)

    user = db.relationship('User', back_populates='comment')
    # group = db.relationship('Group', back_populates='comment')

    def __repr__(self):
        return f'<Comment comment_id={self.comment_id} content={self.content}>'
    
    def as_dict(self):
        return {
            'comment_id': self.comment_id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'content': self.content
        }



def connect_to_db(flask_app, db_uri="postgresql:///collab-todo", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
