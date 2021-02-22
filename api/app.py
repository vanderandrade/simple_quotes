import json
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from apis.Quote import Quote

def create_app(app_name=__name__):
    app = Flask(app_name)
    app.config.from_object('config.DeployConfig')

    from models.model import db
    db.init_app(app)

    return app


app = create_app()
CORS(app)
api = Api(app)


api.add_resource(Quote, '/')
if __name__ == "__main__":
    app.run()