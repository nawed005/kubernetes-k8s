import pika
import time

class Consumer:
    # init method or constructor
    def __init__(self):
        self.credentials = pika.PlainCredentials('guest', 'guest')
        self.parameters = pika.ConnectionParameters(
            '172.16.1.225', 5672, '/', self.credentials)
        try:
            self.connection = pika.BlockingConnection(self.parameters)
        except Exception as error:
            print('Error:', str(error))

    def callback_func(self, ch, method, properties, body):
        print(" [x] Consumer Class callback method Received %r" % body)
        time.sleep(60)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)    

    def recursive_call(self):
        queue_state = self.connection.channel().queue_declare(
            'task_queue', durable=True)
        print("Total no. of messages {}".format(
            queue_state.method.message_count))
        
        if queue_state.method.message_count > 0:
            print("On process from Class Object")
            self.connection.channel().basic_qos(prefetch_count=1)
            method, properties, body = self.connection.channel().basic_get('task_queue')
            self.callback_func(self.connection.channel(),
                               method, properties, body)
            self.recursive_call()  # recursive call
        else:
            print("Queue is empty. No messages to process")
            self.connection.close()

    def main(self):
        print("Consumer Class main method")
        if self.connection.is_open:
            print('Connection is open')
            self.recursive_call()
        else:
            print('Connection is closed')


if __name__ == '__main__':
    obj_consumer = Consumer()
    obj_consumer.main()
