import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


primeSet = "primes"

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<int:number>')
def Prime(number):
	if (number == 1):
		return '{} is not prime\n'.format(number)
		
	if (number == 2):
		cache.sadd(primeSet,number)
		return '{} is prime\n'.format(number)
	if (number == 3):
		cache.sadd(primeSet,number)
		return '{} is prime\n'.format(number)

	if (number % 2 == 0):
		return '{} is not prime\n'.format(number)
	if (number % 3 == 0):
		return '{} is not prime\n'.format(number)

	i=5
	w=2

	while (i*i <= number):
		if (number % i == 0):
			return '{} is not prime\n'.format(number)
		i += w
		w = 6 - w

	cache.sadd(primeSet,number)
	return '{} is prime\n'.format(number)

@app.route('/primesStored')
def printPrimes():
	return '{}\n'.format(cache.smembers(primeSet))
