import pika

connection = pika.BlockingConnection(
                    pika.ConnectionParameters('localhost')
                    )
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch,method,properties,body):
    print('-->',ch,method,properties)
    print("[x] Recieved %r" % body)

channel.basic_consume(callback, #如果收到消息，就调用callback函数来处理消息
                      queue='hello',
                      no_ack=True
                      )

print('[*] Waiting for Messages. To exit press Ctrl-C')
channel.start_consuming()