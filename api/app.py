import json
from flask import Flask
from flask_restful import Api
from models.Quote import Quote

app = Flask(__name__)
api = Api(app)


api.add_resource(Quote, '/')

if __name__ == "__main__":
    app.run()