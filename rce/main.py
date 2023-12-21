from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello World</h1>"

@app.post('/execute')
def execute():
    data = request.json 
    print(data['userCode'])
    return jsonify(data)

if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=True)
