import pika
import time
from os import environ


def callback_func(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(30)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def recursive_call(channel):
    queue_state = channel.queue_declare(queue='task_queue', durable=True)
    print("Total no. of messages {}".format(queue_state.method.message_count))

    if queue_state.method.message_count > 0:
        print("On process")

        channel.basic_qos(prefetch_count=1)
        #channel.basic_consume(queue='task_queue', on_message_callback=callback_func)

        method, properties, body = channel.basic_get('task_queue')
        callback_func(channel, method, properties, body)

        recursive_call(channel)
    else:
        print("Queue is empty. No messages to process")


def main():
    print("In main function")
    rabbitmq_ip = environ.get('BASE_URL').split("//")
    credentials = pika.PlainCredentials(environ.get(
        'RABBITMQ_USER'), environ.get('RABBITMQ_PASSWORD'))
    parameters = pika.ConnectionParameters(
        rabbitmq_ip[1], 5672, '/', credentials)
    try:
        connection = pika.BlockingConnection(parameters)
        if connection.is_open:
            print('Connection is open')
            msg_channel = connection.channel()
            recursive_call(msg_channel)
        else:
            print('Connection is closed')
    except Exception as error:
        print('Error:', str(error))


if __name__ == '__main__':
    main()
