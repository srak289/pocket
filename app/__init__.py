from flask import Flask
import os

from .utils.driver import SQLDriver

sqldriver = SQLDriver()
sqldriver.create_all_tables()

app = Flask(__name__)

from .scanner import Scanner

s = Scanner('172.31.0.0/16')

from . import routes
