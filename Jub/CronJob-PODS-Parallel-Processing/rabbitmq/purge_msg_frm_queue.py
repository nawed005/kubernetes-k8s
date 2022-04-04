import pika
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.16.1.225',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_purge(queue='task_queue')
connection.close()