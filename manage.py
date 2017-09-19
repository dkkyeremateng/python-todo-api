from flask_script import Server

from keep.extensions import manager, db
from keep.app import create_app

# Set the path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

_app = create_app()

manager.app = _app
db.app = _app

# Turn on debugger by default and reloader
manager.add_command("run", Server(
    use_debugger=True,
    use_reloader=True,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 5000))
))

if __name__ == "__main__":
    manager.run()
