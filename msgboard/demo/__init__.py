from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '2lj345hl4hehfl3304pfu8cei13fh4hfe3'

bootstrap = Bootstrap(app)
moment = Moment(app)
CSRFProtect(app)
