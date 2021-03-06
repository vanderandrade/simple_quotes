from flask import request
from flask_restful import Resource
from repository.Quote.QuotePostgresRepository import QuotePostgresRepository

class Quote(Resource):
    """ The quotes View """
    _repository = QuotePostgresRepository()

    def __init__(self, **kwargs):
        if 'repository' in kwargs:
            self._repository = kwargs['repository']

    def get(self):
        """ 
            Returns a list of quotes
        """
        if 'id' in request.args:
            return {'quote': self._repository.get(request.args['id'])}

        if 'filter' in request.args:
            if request.args['filter'] == 'quoters':
                return {'quotes': self._repository.get_all_quoters()}
            elif request.args['filter'] == 'quotes':
                return {'quotes': self._repository.get_all_quotes()}

        return {'quotes': self._repository.get_all()}

    def delete(self):
        """
            Remove stored quote
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
        except:
            pass

        return False

    def post(self):
        """
            Add quote in the storage
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
        except Exception as e:
            print(f'Error: {e}')

        return False

    def put(self):
        '''
            Update stored quote
            Expect a JSON payload with the following format
            {
                "_id": "Quote id for identification",
                "quote": "Updated quote",
                "quote_by": "Updated quoter",
            }
        '''
        data = request.get_json()

        try:
            unchangeable_columns=['added_by', 'id']
            if any(elem in unchangeable_columns for elem in data):
                raise Exception('Invalid fields send for update!')

            if 'quote' in data or 'quote_by' in data:
                self._repository.update(data)
                return True
        except Exception as e:
            print(f'Error: {e}')

        return False


    def _create_quote_object(self, quote, added_by, quoted_by=None, id=None):
        return {'id': id, 'quote': quote, 'quote_by': quoted_by, 'added_by': added_by}
