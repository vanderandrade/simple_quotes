from flask import request
from flask_restful import Resource
from redis import Redis

redis = Redis(host='redis', port=6379, decode_responses=True)

class Quote(Resource):
    """ The quotes View """
    _QUOTE_KEY='quote'

    def get(self):
        """ Returns a list of quotes """
        redis.incr('get_quote')
        print(f"Quotes has been viewed {redis.get('get_quote')} time(s).")

        quote = redis.hgetall(self._QUOTE_KEY)
        quotes = [quote] if quote else []

        return { 'quotes': quotes }

    def post(self):
        """
        Add a quote to redis
        Expect a JSON payload with the following format
        {
            "quote": "The quote",
            "quote_by": "The person who said the quote"
        }
        """
        data = request.get_json()

        try:
            if 'quote' in data and 'quote_by' in data and 'added_by' in data:
                redis.incr('post_quote')
                id=redis.get('post_quote')

                quote = self._create_quote_object(id, data['quote'], data['quote_by'], data['added_by'])
                redis.hmset(self._QUOTE_KEY, quote)

                return True

            return False
        except:
            return False


    def _create_quote_object(self, id, quote, quoted_by, added_by):
        return {'id': id, 'quote': quote, 'quote_by': quoted_by, 'added_by': added_by}
