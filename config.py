from pathlib import Path

from environs import Env
import redis


BASE_DIR = Path(__file__).resolve().parent

env = Env()
env.read_env('.env')

pool = redis.ConnectionPool(host=env('REDIS_HOST'), port=env('REDIS_PORT'), db=0, decode_responses=True)
redis = redis.Redis(connection_pool=pool)
