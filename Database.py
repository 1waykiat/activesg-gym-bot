# Obsolete class, to be removed in future

import redis
from redis.exceptions import AuthenticationError, ConnectionError
from dotenv import load_dotenv
import os

load_dotenv()

# Loaded from environment or secrets
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

class Database:
    def connect_to_redis():
        try:
            r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True
            )

            r.ping()
            return r
        except AuthenticationError:
            print("Authentication Failed. Please check your password.")
            return None
        except ConnectionError:
            print("Failed to connect to Redis. Please check your host and port.")
            return None
        except Exception as e:
            print(f"An error occured: {str(e)}")
            return None
        
        
