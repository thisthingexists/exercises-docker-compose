import os
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)

@app.route("/")
def index():
    return f"Hello! This page has been visited {redis.incr('hits')} times.\n"
