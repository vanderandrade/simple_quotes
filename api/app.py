import json
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from apis.Quote import Quote
from apis.Healthcheck import Healthcheck
from repository.Quote.QuoteRedisRepository import QuoteRedisRepository
from repository.Quote.QuotePostgresRepository import QuotePostgresRepository

def create_app(app_name=__name__, environment='local', storage='postgres'):
    app = Flask(app_name)

    if environment == 'test':
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.DeployConfig')

    from models.model import db
    db.init_app(app)

    CORS(app)
    api = Api(app)

    quote_repository = QuotePostgresRepository() if storage == 'postgres' else QuoteRedisRepository()

    api.add_resource(Healthcheck, '/')
    api.add_resource(Quote, '/quotes', resource_class_kwargs={'repository': quote_repository})

    return app

app = create_app()

if __name__ == "__main__":
    app.run()