import pika
import sys
import os


def main():
    print("In main function")
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('172.16.1.225',
                                           5672,
                                           '/',
                                           credentials)
    try:
        connection = pika.BlockingConnection(parameters)
        if connection.is_open:
            print('Connection is open')

            channel = connection.channel()
            channel.queue_declare(queue='task_queue', durable=True)

            def callback(ch, method, properties, body):
                #print(" [x] Received %r" % body)
                print(type(body.decode()))
                print(" [x] Received %r" % body.decode())

            channel.basic_consume(
                queue='task_queue', on_message_callback=callback, auto_ack=True)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

    except Exception as error:
        print('Error:', error.__class__.__name__)


if __name__ == '__main__':
    main()
