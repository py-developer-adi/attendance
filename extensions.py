'''PyCODE | @_py.code'''

# ? Importing Libraries
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract, func
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_socketio import SocketIO
from flask_migrate import Migrate
from datetime import datetime, date
from collections import defaultdict
from werkzeug.security import check_password_hash, generate_password_hash

# ! EXTENSION INITIALIZATIONS
db = SQLAlchemy()
logger = LoginManager()
socket = SocketIO()
migrate = Migrate()

# | User Model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    
    def get_id(self):
        return self.id
    
# | Attendee Model
class Attendee(db.Model):
    __tablename__ = 'attendee'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    manager = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    mobile = db.Column(db.String)
    
# | Attendance Model
class Attendance(db.Model):
    __tablename__ = 'attendance'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String, primary_key=True)
    attendee = db.Column(db.String, nullable=False)
    attender = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False)
    
# | Help Model
class Help(db.Model):
    __tablename__ = 'help'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    help = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, default=False)