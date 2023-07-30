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
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(30), nullable=False, unique=True)
    private = db.Column(db.Boolean, nullable=False, default=True)

    user_groups = db.relationship('UserGroup', back_populates='group')

    def __repr__(self):
        return f'<Group group_id={self.group_id} name={self.name}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def as_dict(self):
        return {
            'group_id': self.group_id,
            'name': self.name,
            'private': self.private
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