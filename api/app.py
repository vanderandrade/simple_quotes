from flask import Flask, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    return 'OK', 200

@app.route('/quote', methods=['GET'])
def get_redis():
    redis.incr('get_quote')
    print(f"Quotes has been viewed {redis.get('get_quote')} time(s).")

    quote = redis.get('quote')
    if quote:
        return quote, 200
    return 'We don\'t hava a quote at this moment!', 200

@app.route('/quote', methods=['POST'])
def post_redis():
    quote=request.form.get('quote')

    redis.set('quote', quote)

    redis.incr('post_quote')
    print(f"Quote has been changed {redis.get('post_quote')} time(s).")
    return 'OK'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)