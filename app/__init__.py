from flask import Flask
from config import Config, DevConfig, ProdConfig
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_qr import QR

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socket = SocketIO(app)
#socket.init_app(app, cors_allowed_origins="*")
#enable at deployment!


login = LoginManager(app)

qr = QR(app, mode="google")

from app import routes,models