from repository.AbstractRepository import AbstractRepository
from storage import redis

class QuoteRedisRepository(AbstractRepository):
    _QUOTE_KEY='quote'
    _GET_QUOTE='get_quote'
    _ID_QUOTE='id_quote'

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

            redis.hmset(id, quote)
            redis.lpush(self._QUOTE_KEY, id)

            return True
        except:
            return False

    def get(self, reference):
        quote = redis.hgetall(reference)

        if quote:
            return quote
        return None

    def get_all(self):
        quotes=[]
        for id in redis.lrange(self._QUOTE_KEY, 0, -1 ):
            quotes.append(redis.hgetall(id))
        return quotes

    def delete(self, reference):
        try:
            redis.lrem(self._QUOTE_KEY, 0, int(reference))
            redis.delete(reference)

            return True
        except:
            return False