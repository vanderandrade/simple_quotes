from redis import Redis
import fakeredis

def get_mock_redis():
    server = fakeredis.FakeServer()
    return fakeredis.FakeStrictRedis(server=server, decode_responses=True)


redis = Redis(host='redis', port=6379, decode_responses=True)