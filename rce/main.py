import subprocess
import pika
import threading
import json


# RabbitMQ connection parameters
rabbitmq_params = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest'),
    virtual_host='/'
)


consume_next_task = threading.Event()


def execute_python_code(body):
    input_str = body.decode('utf-8')
    data = json.loads(input_str)
    code_value = data.get('code')
    userId = data.get("userId")

    try:
        with open("./user_code.py", 'w') as file:
            file.write(code_value)
        
        result = subprocess.check_output(['python', './user_code.py'], text=True, timeout=10)
        return {"result": result, "userId": userId}
    except Exception as e:
        print("Error Executing the python code")


# Get Result Back
def send_result_back(result):
    try:
        connection = pika.BlockingConnection(rabbitmq_params)
        channel = connection.channel()

        queue_name = "result"
        channel.queue_declare(queue=queue_name, durable=False)

        result_message = json.dumps(result)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=result_message
        )

        print(f"Result sent to queue '{queue_name}': {result_message}")

        connection.close()
    except Exception as e:
        print(f"Error sending result to queue: {e}")


# Get task from more task.
def consume_task():
    try:
        print("Consuming messages from 'task' queue")
        connection = pika.BlockingConnection(rabbitmq_params)
        channel = connection.channel()

        queue_name = 'task'
        channel.queue_declare(queue=queue_name, durable=False)

        # Callback function to handle incoming messages
        def callback(ch, method, properties, body):
            result = execute_python_code(body)
            print("Task processing completed")
            send_result_back(result)
            consume_next_task.set()

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print("Waiting for messages. To exit press Ctrl+C")
        channel.start_consuming()
    except Exception as e:
        print(f"Error consuming task: {e}")



if __name__ == "__main__":
    threading.Thread(target=consume_task).start()