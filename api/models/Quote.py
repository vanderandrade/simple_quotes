from flask import request
from flask_restful import Resource
from repository.Quote.QuoteRedisRepository import QuoteRedisRepository

class Quote(Resource):
    """ The quotes View """
    _repository = QuoteRedisRepository()

    def get(self):
        """ 
            Returns a list of quotes
        """
        quotes = self._repository.get_all()

        quoters = self._repository.get_all_quoters()
        print(quoters)

        quoterss = self._repository.get_all_quotes()
        print(quoterss)
        return {'quotes': quotes}

    def delete(self):
        """
            Remove quote from redis
            Expect a JSON payload with the following format
            {
                "quote_id": "The id of quote to be removed"
            }
        """
        data = request.get_json()

        try:
            if 'quote_id' in data:
                self._repository.delete(data['quote_id'])

                return True
            return False
        except:
            return False

    def post(self):
        """
            Add a quote to redis
            Expect a JSON payload with the following format
            {
                "quote": "The quote",
                "quote_by": "The person who said the quote",
                "added_by": "The person who is posting the quote"
            }
        """
        data = request.get_json()

        try:
            if 'quote' in data and 'added_by' in data:
                quote = self._create_quote_object(
                    data['quote'],
                    data['added_by'],
                    data['quote_by'] if 'quote_by' in data and data['quote_by'] else None
                )
                self._repository.add(quote)

                return True
        except:
            pass

        return False


    def _create_quote_object(self, quote, added_by, quoted_by=None, id=None):
        return {'id': id, 'quote': quote, 'quote_by': quoted_by, 'added_by': added_by}
