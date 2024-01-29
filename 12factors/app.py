import os
from flask import Flask
from redis import Redis

app = Flask(__name__)
redisDb = Redis(host=os.getenv('HOST'), port=os.getenv('PORT'))

@app.route('/')
def welcomeToKodeKloud():
    redisDb.incr('visitCount')
    visitCount = str(redisDb.get('visitCount'), 'utf-8')
    return "Welcome to KodeKloud! Visit Count: " + visitCount + "\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
