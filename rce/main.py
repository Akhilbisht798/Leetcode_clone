from flask import Flask, request, jsonify, make_response
import subprocess
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello World</h1>"

# Add more languge such as js, c++, java.
# And make more function for them.
@app.post('/execute')
def execute():
    data = request.json 
    code = data['userCode']
    try:
        with open("./user_code.py", 'w') as file:
            file.write(code)

        result = subprocess.check_output(['python', './user_code.py'], text=True, timeout=10)
        return jsonify({'result': result})
    except Exception as e:
        print("Error Executing the python code")
        return jsonify({'error': f'Error executing the code: {str(e)}'}), 500

if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=True)