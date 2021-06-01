#!usrbinenv python
import pika
import sys
import csv
import os
from os import environ
import re
from datetime import datetime, date, timedelta
import pathlib

class CreateMsgQueue:

    ingredient_files_path = os.getcwd()+"/data/input/ingredient_consumption/"

    def rename_csv(self, file_path,recent_file_name,actual_file_name,file_sufix):
        os.rename(file_path + recent_file_name +'.csv',file_path + actual_file_name + '_' + file_sufix + '.csv')


    def parse_files(self):
        today = date.today().strftime('%d%m%Y')
        getfiles = list(pathlib.Path(self.ingredient_files_path).glob('*_'+today+'.csv'))
        # getfiles.extend(list(pathlib.Path(self.ingredient_files_path).glob('*_'+today+'_error.csv')))
        print(getfiles)
        
        
        for files in getfiles:
            arr_filename = re.split('_', os.path.splitext(os.path.basename(files))[0])
            self.rename_csv(self.ingredient_files_path, arr_filename[0]+'_'+arr_filename[1], arr_filename[0]+'_'+arr_filename[1],'prog')
            self.push_file_to_queue(arr_filename[0]+'_' + arr_filename[1]+'_prog.csv')


    def push_file_to_queue(self,file_name):

        rabbitmq_ip = environ.get('BASE_URL').split("//")
        credentials = pika.PlainCredentials(environ.get('RABBITMQ_USER'), environ.get('RABBITMQ_PASSWORD'))
        parameters = pika.ConnectionParameters(rabbitmq_ip[1],
                                            5672,
                                            '/',
                                            credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()


        channel.queue_declare(queue='task_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=file_name,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        #print( "[x] Sent %r % message")
        print("File sent to Queue after renamed {}".format(file_name))
        connection.close()

if __name__ == "__main__":
    obj=CreateMsgQueue()
    obj.parse_files()

