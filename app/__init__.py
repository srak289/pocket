from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mako import MakoTemplates
import os

file_path = os.path.abspath(os.getcwd())+"/crap.db"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
db.create_all()

app.secret_key = b'\xafbr#\x13\x9d\xd5\xbeP\xad\xe1\x93}h\xa6\xdc\x8e\xf1\xff\xd8Z\xea\xed\xf4'

app.template_folder = 'templates'
mako = MakoTemplates(app)

from app import routes
