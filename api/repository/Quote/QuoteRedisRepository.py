from repository.AbstractRepository import AbstractRepository
from storage import redis, get_mock_redis
from utils.definitions import QuoteAction

class QuoteRedisRepository(AbstractRepository):
    _redis=get_mock_redis()

    _QUOTE_KEY='quote'
    _ID_QUOTE='id_quote'
    _NULL_VALUE='NULL'

    def __init__(self, **kwargs):
        if 'environment' in kwargs and kwargs['environment'] == 'test':
            self._redis = get_mock_redis()
        else:
            self._redis = redis


    def add(self, quote):
        if quote is None:
            raise ValueError

        if 'quote' not in quote or 'added_by' not in quote:
            raise ValueError

        if 'quote_by' not in quote or not quote['quote_by']:
            quote['quote_by'] = 'Unknown'

        try:
            if 'id' in quote and quote['id'] != None:
                id = quote['id']
            else:
                self._redis.incr(self._ID_QUOTE)
                id=self._redis.get(self._ID_QUOTE)
                quote['id'] = id

            quote = self._convert_quote_null_values(quote)
            self._redis.hmset(id, quote)
            self._redis.lpush(self._QUOTE_KEY, id)

            return True
        except Exception as e:
            print(f'Error: {e}')

        return False

    def get(self, reference):
        quote = self._redis.hgetall(reference)

        if quote:
            quote = self._convert_quote_null_values(quote, to_null=True)
            return quote
        return None

    def get_all(self):
        return self._get_all(QuoteAction.GET_ALL)

    def get_all_quotes(self):
        return self._get_all(QuoteAction.GET_ALL_QUOTES)

    def get_all_quoters(self):
        return self._get_all(QuoteAction.GET_ALL_QUOTERS)
        

    def delete(self, reference):
        try:
            self._redis.lrem(self._QUOTE_KEY, 0, int(reference))
            self._redis.delete(reference)

            return True
        except Exception as e:
            print(f'Error: {e}')
            return False


    def _get_all(self, action: QuoteAction):
        result=[]
        for id in self._redis.lrange(self._QUOTE_KEY, 0, -1 ):
            if action == QuoteAction.GET_ALL:
                quote = self._convert_quote_null_values(self._redis.hgetall(id), to_null=True)
                result.append(quote)
            else:
                quote = self._convert_quote_null_values(self._redis.hget(id, action.value), to_null=True)
                if quote not in result:
                    result.append(quote)

        
        if action == QuoteAction.GET_ALL and result:
            return sorted(result, key=lambda k: k['id']) 
        return sorted(result)

    def _convert_quote_null_values(self, quote, to_null=False):
        original_value= self._NULL_VALUE if to_null else None
        converted_value= None if to_null else self._NULL_VALUE

        if isinstance(quote, dict):
            for k, v in quote.items():
                if v is original_value or v == original_value:
                    quote[k] = converted_value
        else:
            if quote is original_value or quote == original_value:
                quote = converted_value

        return quote