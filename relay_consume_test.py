#!/usr/bin/env python
import pika
import sys


credentials = pika.PlainCredentials('vu_relay', 'password')
parameters = pika.ConnectionParameters(host = '0.0.0.0',
                                       port = 5672,
                                       virtual_host = 'VU',
                                       credentials = credentials)
print parameters
print 'ping'
connection = pika.BlockingConnection(parameters)
print 'pong'
channel = connection.channel()

channel.exchange_declare(exchange='RELAY_FB',
                         exchange_type='topic',
                         durable=True)
print 'ping'
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

print 'queue name:', queue_name
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    print binding_key
    channel.queue_bind(exchange='RELAY_FB',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
