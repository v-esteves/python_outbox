import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/v1/user', methods=['POST'])
def registration():
    json = request.get_json()
    
    name = json["name"]
    email = json["email"]

    db = redis.Redis(host='localhost',port=6379, charset="utf-8", decode_responses=True)

    transaction = db.pipeline()
    transaction.set(json["email"],json["name"])
    transaction.rpush('emails',json["email"])
    transaction.execute()

    nameFromRedis = db.get(json["name"])
    
    return "JSON name sent: "+str(nameFromRedis)