import json
from datetime import datetime, date

import pytest
from flask_migrate import Migrate

from app import create_app
from models.model import db


@pytest.fixture(scope="module")
def app_postgres():
    app = create_app(environment='test', storage='postgres')
    with app.app_context():
        db.create_all()
        Migrate(app, db)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def app_redis():
    app = create_app(environment='test', storage='redis')
    with app.app_context():
        db.create_all()
        Migrate(app, db)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.mark.order1
def test_get_empty_db(app_postgres):
    r = app_postgres.test_client().get('/quotes')

    assert r.status_code == 200
    assert r.json['quotes'] == []

@pytest.mark.order1
def test_delete_empty_db(app_postgres):
    r = app_postgres.test_client().delete('/quotes')
    print(r.json)

    assert r.status_code == 200
    assert r.json == False

@pytest.mark.order1
def test_add_invalid_quote_object(app_postgres):
    quote = {'quote': 'Lorem Ipsum', 'quote_by': 'Lorem'}
    r = app_postgres.test_client().post('/quotes', json=quote)

    assert r.status_code == 200
    assert r.json == False

    quote = {'added_by': 'Lorem Ipsum', 'quote_by': 'Lorem'}
    r = app_postgres.test_client().post('/quotes', json=quote)

    assert r.status_code == 200
    assert r.json == False

@pytest.mark.order1
def test_add_valid_quote_objects(app_postgres):
    quote = {'quote': 'Lorem Ipsum', 'added_by': 'Lorem', 'quote_by': 'Ipsum'}
    r = app_postgres.test_client().post('/quotes', json=quote)

    assert r.status_code == 200
    assert r.json == True

    quote = {'quote': 'Lorem Ipsum', 'added_by': 'Lorem'}
    r = app_postgres.test_client().post('/quotes', json=quote)

    assert r.status_code == 200
    assert r.json == True

@pytest.mark.order2
def test_get_quotes(app_postgres):
    r = app_postgres.test_client().get('/quotes')

    assert r.status_code == 200
    assert {'quote': 'Lorem Ipsum', 'added_by': 'Lorem', 'quote_by': 'Ipsum'} in r.json['quotes']
    assert {'quote': 'Lorem Ipsum', 'added_by': 'Lorem', 'quote_by': 'Unknown'} in r.json['quotes']
