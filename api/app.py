import json
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from apis.Quote import Quote
from apis.Healthcheck import Healthcheck

def create_app(app_name=__name__, environment='local'):
    app = Flask(app_name)

    if environment == 'test':
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.DeployConfig')

    from models.model import db
    db.init_app(app)

    return app


app = create_app()
CORS(app)
api = Api(app)


api.add_resource(Healthcheck, '/')
api.add_resource(Quote, '/quotes')
if __name__ == "__main__":
    app.run()