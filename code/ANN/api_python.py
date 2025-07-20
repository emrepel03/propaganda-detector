from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')  # Decode the raw data as UTF-8
    # Process the data or perform actions
    response = {"message": "Received text:", "data": data}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
