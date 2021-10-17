import pika
import redis
import datetime, threading
import configparser

#Read configurations
parser = configparser.ConfigParser()
parser.read("config.py")

#Connect to rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters(host=parser.get('RABBIT','RABBITMQ_ENDPOINT'),
                                                                port=parser.get('RABBIT','RABBITMQ_PORT')))
channel = connection.channel()
channel.queue_declare(queue=parser.get('RABBIT','RABBITMQ_QUEUE'))

# Connect to Redis 
db = redis.Redis(host=parser.get('REDIS','REDIS_ENDPOINT'),
                 port=parser.get('REDIS','REDIS_PORT'), 
                 charset="utf-8", 
                 decode_responses=True)

def sendMessage(email):
    channel.basic_publish(exchange='', routing_key='user', body=email)

def pullFromRedis():
    print(datetime.datetime.now())
    print('Fetching Redis queue for emails')

    email = str(db.rpop('emails'))

    if not email:
        sendMessage(email)
        print('Message for '+email+' sent')
    else:
        print('Empty queue')

    threading.Timer(10, pullFromRedis).start()

if __name__ == '__main__':

    try:
        pullFromRedis()

    except KeyboardInterrupt:
        print('Interrupted')
        connection.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    


