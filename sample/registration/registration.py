import redis
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/api/v1/user', methods=['POST'])
def registration():
    json = request.get_json()

    # Connect to Redis 
    db = redis.Redis(host=app.config['REDIS_ENDPOINT'],
                        port=app.config['REDIS_PORT'], 
                        charset="utf-8", 
                        decode_responses=True)

    # Create a "transaction" to execute both commands or don't execute
    # We need to have total assurance that both data is stored
    transaction = db.pipeline()
    transaction.set(json["email"],json["name"])
    # Redis Lists are used to create a queue for the dispatcher work
    transaction.rpush('emails',json["email"])
    transaction.execute()

    # Fetch name to return
    nameFromRedis = db.get(json["email"])
    
    return "Name sent: "+str(nameFromRedis)