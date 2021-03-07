from flask import request
from flask_restful import Resource

class Healthcheck(Resource):
    """ The Healthcheck View """

    def get(self):
        """ 
            Returns if the application is alive
        """
        return 'OK', 200
