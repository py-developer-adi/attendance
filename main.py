'''PyCODE | @_py.code'''

# ? Importing Libraries
from flask import Flask
from extensions import *
from routes import *

# ! SERVER INITIALIZATION
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.config['SECRET_KEY'] = 'management.attendance-pycode'

# ! EXTENSION INITIALIZATION
db.init_app(server)
logger.init_app(server)
socket.init_app(server)
migrate.init_app(server, db)
server.register_blueprint(router)

# // /attendance