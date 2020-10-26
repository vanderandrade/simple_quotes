from flask import request
from flask_restful import Resource
from redis import Redis

redis = Redis(host='redis', port=6379)

class Quote(Resource):
    """ The quotes View """

    def get(self):
        """ Returns a list of quotes """

        redis.incr('get_quote')
        print(f"Quotes has been viewed {redis.get('get_quote')} time(s).")

        quote = redis.get('quote')
        if quote:
            quotes = [{ "id":1, "quote": quote.decode('utf-8')}]

        return { 'quotes': quotes }

    def post(self):
        """
        Add a quote to the redis
        Expect a JSON payload with the following format
        {
            "quote": "The quote"
        }
        """
        data = request.get_json()

        try:
            if 'quote' in data:
                redis.set('quote', data['quote'])

                redis.incr('post_quote')
                print(f"Quote has been changed {redis.get('post_quote')} time(s).")
                return True

            return False
        except:
            return False