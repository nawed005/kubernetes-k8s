#!usrbinenv python
import pika
import sys

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.16.1.225',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
#print( "[x] Sent %r % message")
print("Message Sent {}".format(message))
connection.close()
