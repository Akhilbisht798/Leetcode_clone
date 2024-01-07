from flask import Flask, request, jsonify, make_response
import subprocess
import pika
import threading
import json
# app = Flask(__name__)


# RabbitMQ connection parameters
rabbitmq_params = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest'),
    virtual_host='/'
)

consume_next_task = threading.Event()

# @app.route("/")
# def hello_world():
#     return "<h1>Hello World</h1>"


# # Add more languge such as js, c++, java.
# # And make more function for them.
# @app.post('/execute')
# def execute():
#     data = request.json 
#     code = data['userCode']
#     try:
#         with open("./user_code.py", 'w') as file:
#             file.write(code)

#         result = subprocess.check_output(['python', './user_code.py'], text=True, timeout=10)
#         return jsonify({'result': result})
#     except Exception as e:
#         print("Error Executing the python code")
#         return jsonify({'error': f'Error executing the code: {str(e)}'}), 500

def execute_python_code(body):
    input_str = body.decode('utf-8')
    data = json.loads(input_str)
    code_value = data.get('code')
    userId = data.get("userId")

    try:
        with open("./user_code.py", 'w') as file:
            file.write(code_value)
        
        result = subprocess.check_output(['python', './user_code.py'], text=True, timeout=10)
        return result
    except Exception as e:
        print("Error Executing the python code")


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
            print(f"Received task: {body}")
            result = execute_python_code(body)
            print(result)
            print("Task processing completed")
            consume_next_task.set()

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print("Waiting for messages. To exit press Ctrl+C")
        channel.start_consuming()
    except Exception as e:
        print(f"Error consuming task: {e}")



if __name__ == "__main__":
    threading.Thread(target=consume_task).start()
    # app.run(host="0.0.0.0", port=5000, debug=True)
