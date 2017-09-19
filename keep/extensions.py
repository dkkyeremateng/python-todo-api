from flask_script import Manager
from flask_mongoengine import MongoEngine

manager = Manager()
db = MongoEngine()
