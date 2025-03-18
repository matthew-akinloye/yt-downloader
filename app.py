# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')  # Fallback to SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://default:JWxPWqicyVxlVEwpHJR927Hck1I4PRl1@redis-12216.c245.us-east-1-3.ec2.redns.redis-cloud.com:12216')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://default:JWxPWqicyVxlVEwpHJR927Hck1I4PRl1@redis-12216.c245.us-east-1-3.ec2.redns.redis-cloud.com:12216')
app.config['DEBUG']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes after initializing the app to avoid circular imports
import routes