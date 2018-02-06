#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('vu_relay', 'password')
parameters = pika.ConnectionParameters(host = '0.0.0.0',
                                       port = 5672,
                                       virtual_host = 'VU',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()


#channel.exchange_declare(exchange='RELAY_FB',
#                         exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='RELAY_FB',
                      routing_key=routing_key,
                      body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()
