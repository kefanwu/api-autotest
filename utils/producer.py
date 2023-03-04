import pika


class MqTools():

    def producer(self, test_msg):
        python_exchange = 'python_exchange'
        routingKey = 'python_routing_key'
        python_queue = 'python_queue'
        # 1 建立rabbit连接通道
        credentials = pika.PlainCredentials('admin', 'admin')  # 用户名，密码
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
        channel = connection.channel()
        # 2 定义交换机名称和交换机类型
        # exchange: 交换机名称，可以自定义
        # exchange_type: 交换机类型，默认就是直连的
        channel.exchange_declare(exchange=python_exchange,  exchange_type='direct')
        # 定义路由键信息
        # 3 定义队列，绑定交换机 durable=True：队列持久化
        channel.queue_declare(queue=python_queue, durable=True, auto_delete=True)
        channel.queue_bind(exchange=python_exchange, queue=python_queue, routing_key=routingKey)
        # 4 发布消息
        # properties=pika.BasicProperties(delivery_mode=2, ) 持久化队列中的消息
        test_msg1 = 'this is a demotest 8888888888'
        channel.basic_publish(exchange=python_exchange, routing_key=routingKey, body=test_msg,
                              properties=pika.BasicProperties(delivery_mode=2, ))
        # 关闭连接
        connection.close()



