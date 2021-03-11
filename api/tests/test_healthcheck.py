import json
from datetime import datetime, date

import pytest
from flask_migrate import Migrate

from app import create_app
from models.model import db


@pytest.fixture(scope="module")
def app():
    app = create_app(environment='test')
    with app.app_context():
        db.create_all()
        Migrate(app, db)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.mark.order1
def test_healthcheck(app):
    r = app.test_client().get('/')

    assert r.status_code == 200
    assert r.json == 'OK'
