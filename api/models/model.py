import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quote(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    quote = db.Column(db.String(100))
    quote_by = db.Column(db.String(100), server_default='Unknown')
    added_by = db.Column(db.String(100))
