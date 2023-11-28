from flask import Flask
from flask_ import SQLAlchemy

app = Flask(__name__)

from fakepinterest import routes