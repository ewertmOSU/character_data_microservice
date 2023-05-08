#!/usr/bin/env python
import pika, sys, os

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_character_queue')


def fetch_character(char_name: str) -> str:
    print(char_name)
    # concatenante the file name from the character name
    # ie. ./characters/mario.txt
    filename = "./characters/" + char_name + ".txt"
    file = open(filename)
    # this reads the first line of the file
    char_data = file.readline()
    return char_data

def on_request(ch, method, props, body):
    # event body contains the characters name
    name = body.decode()

    print(f'looking up character: {name}')
    # fetch character data to send response
    response = fetch_character(name)

    # publish a message containing the character data and the correlation id
    # from the request.
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))

    # acknowledge that the message containing the request has been received
    # and processed
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(queue='rpc_character_queue', on_message_callback=on_request)
  channel.start_consuming()

if __name__ == '__main__':
    try:
        print(" [x] Awaiting RPC requests. Ctrl + C to quit")
        main()

    # allow signals to interrupt the server
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

