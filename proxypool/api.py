from flask import Flask, jsonify, g
import os
from db import RedisClient

app = Flask(__name__)


# app.config.update(dict(
#     HOST='localhost',
#     PORT=6379
# ))

def get_conn():
    """Opens a new redis connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'redis_client'):
        g.redis_client = RedisClient()
    return g.redis_client

@app.route('/')
def index():
    return '<h1>Welcome</h1>'

@app.route('/get')
def get_proxy():
    conn = get_conn()
    return conn.pop()

@app.route('/counts')
def get_counts():
    conn = get_conn()
    return conn.queue_len

if __name__ == '__main__':
    app.run()
