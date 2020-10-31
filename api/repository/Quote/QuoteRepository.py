from repository.AbstractRepository import AbstractRepository
from storage import redis

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
        quotes=[]
        for id in redis.lrange(self._QUOTE_KEY, 0, -1 ):
            quote = self._convert_quote_null_values(redis.hgetall(id), to_null=True)
            quotes.append(quote)
        return quotes

    def delete(self, reference):
        try:
            redis.lrem(self._QUOTE_KEY, 0, int(reference))
            redis.delete(reference)

            return True
        except:
            return False


    def _convert_quote_null_values(self, quote, to_null=False):
        original_value= self._NULL_VALUE if to_null else None
        converted_value= None if to_null else self._NULL_VALUE
        for k, v in quote.items():
            if v is original_value or v == original_value:
                quote[k] = converted_value

        return quote