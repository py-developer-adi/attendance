'''PyCODE | @_py.code'''

# ? Importing Server
from main import *

# ! RUN THE SERVER
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
        
    socket.run(server, debug=False, host='0.0.0.0', allow_unsafe_werkzeug=True)
