from flask import Flask, jsonify
import os
from db import RedisClient

app = Flask(__name__)

conn = RedisClient()

# app.config.update(dict(
#     HOST='localhost',
#     PORT=6379
# ))


@app.route('/')
def index():
    return '<h1>Welcome</h1>'

@app.route('/get')
def get_proxy():
    return conn.pop()

@app.route('/counts')
def get_counts():
    return conn.queue_len

if __name__ == '__main__':
    app.run()
