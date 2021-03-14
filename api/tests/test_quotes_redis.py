import json
import pytest
from datetime import datetime, date
from flask_migrate import Migrate
from app import create_app
from models.model import db


@pytest.fixture(scope="module")
def app():
    app = create_app(environment='test', storage='redis')
    with app.app_context():
        db.create_all()
        Migrate(app, db)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.mark.order1
def test_get_empty_db(app):
    r = app.test_client().get('/quotes')

    assert r.status_code == 200
    assert r.json['quotes'] == []

@pytest.mark.order1
def test_delete_empty_db(app):
    r = app.test_client().delete('/quotes')
    print(r.json)

    assert r.status_code == 200
    assert r.json == False

@pytest.mark.order1
def test_add_invalid_quote_object(app):
    quote = {'quote': 'Lorem Ipsum', 'quote_by': 'Lorem'}
    r = app.test_client().post('/quotes', json=quote)

    assert r.status_code == 200
    assert r.json == False

    quote = {'added_by': 'Lorem Ipsum', 'quote_by': 'Lorem'}
    r = app.test_client().post('/quotes', json=quote)

    assert r.status_code == 200
    assert r.json == False

@pytest.mark.order1
def test_add_valid_quote_objects(app):
    quote = {'quote': 'Lorem Ipsum', 'added_by': 'Lorem', 'quote_by': 'Ipsum'}
    r = app.test_client().post('/quotes', json=quote)

    assert r.status_code == 200
    assert r.json == True

    quote = {'quote': 'Lorem Ipsum', 'added_by': 'Lorem'}
    r = app.test_client().post('/quotes', json=quote)

    assert r.status_code == 200
    assert r.json == True

@pytest.mark.order2
def test_get_full_quotes(app):
    r = app.test_client().get('/quotes', json={})

    assert r.status_code == 200
    assert {'quote': 'Lorem Ipsum', 'added_by': 'Lorem', 'quote_by': 'Ipsum', 'id': '1'} in r.json['quotes']
    assert {'quote': 'Lorem Ipsum', 'added_by': 'Lorem', 'quote_by': 'Unknown', 'id': '2'} in r.json['quotes']

@pytest.mark.order2
def test_get_quoters(app):
    r = app.test_client().get('quotes', query_string={'filter': 'quoters'})

    assert r.status_code == 200
    assert ['Unknown', 'Ipsum'] == r.json['quotes']

@pytest.mark.order2
def test_get_quotes(app):
    r = app.test_client().get('quotes', query_string={'filter': 'quotes'})
    print(r.json)

    assert r.status_code == 200
    assert ['Lorem Ipsum'] == r.json['quotes']


