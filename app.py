import time
import math

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

#def get_hit_count():
#    retries = 5
#    while True:
#        try:
#            return cache.incr('hits')
#        except redis.exceptions.ConnectionError as exc:
#            if retries == 0:
#                raise exc
#            retries -= 1
#            time.sleep(0.5)
def stored_primes():
    return str(cache.lrange('primes',0,-1)) + '\n'
def detect_num(n):
    if n == 0 or n == 1:
        return False
    if n <= 3 and n > 1:
        cache.lpush('primes', n)
        return True
    if n%6 != 1 and n%6 != 5:
        return False
    else:
        sqrt = math.sqrt(n)
        x = 5
        while(x < sqrt):
            if n%x == 0 or n%(x+2) == 0:
                return False
            else:
                x=x+6
        cache.lpush('primes', n)
        return True
@app.route('/isPrime/<int:number>')
#def hello():
#    count = get_hit_count()
#    return 'Hello World! I have been seen {} times.\n'.format(count)
 
def detect(number):
    status = detect_num(number)
    if status:
        return '{} is prime\n'.format(number)
    else:
        return '{} is not prime\n'.format(number)

@app.route('/primesStored')

def display():
    return stored_primes()
