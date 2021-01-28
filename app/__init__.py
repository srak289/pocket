from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mako import MakoTemplates
import os

from app.scanner import Scanner

file_path = os.path.abspath(os.getcwd())+"/pocket.db"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
db.create_all()

s = Scanner('55.35.0.0/16')

app.secret_key = b"\x0bA\xb5\x8b@g\x92'\x8b\xd6\x1b\xa3(!\xdd\xc0\r\xb7\x80kgUt`"

app.template_folder = 'templates'
mako = MakoTemplates(app)

from app import routes
