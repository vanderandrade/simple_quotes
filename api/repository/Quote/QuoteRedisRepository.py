from repository.AbstractRepository import AbstractRepository
from storage import redis
from utils.definitions import QuoteAction

class QuoteRedisRepository(AbstractRepository):
    _QUOTE_KEY='quote'
    _ID_QUOTE='id_quote'
    _NULL_VALUE='NULL'

    def add(self, quote):
        if quote is None:
            raise ValueError

        if 'quote' not in quote or 'added_by' not in quote:
            raise ValueError

        try:
            if 'id' in quote and quote['id'] != None:
                id = quote['id']
            else:
                redis.incr(self._ID_QUOTE)
                id=redis.get(self._ID_QUOTE)
                quote['id'] = id

            quote = self._convert_quote_null_values(quote)
            redis.hmset(id, quote)
            redis.lpush(self._QUOTE_KEY, id)

            return True
        except:
            pass

        return False

    def get(self, reference):
        quote = redis.hgetall(reference)

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
            redis.lrem(self._QUOTE_KEY, 0, int(reference))
            redis.delete(reference)

            return True
        except:
            return False


    def _get_all(self, action: QuoteAction):
        result=[]
        for id in redis.lrange(self._QUOTE_KEY, 0, -1 ):
            if action == QuoteAction.GET_ALL:
                quote = self._convert_quote_null_values(redis.hgetall(id), to_null=True)
                result.append(quote)
            else:
                quote = self._convert_quote_null_values(redis.hget(id, action.value), to_null=True)
                if quote not in result:
                    result.append(quote)

        return result

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