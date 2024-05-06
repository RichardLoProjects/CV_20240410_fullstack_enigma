from flask import Flask, request, jsonify
from enigma_machine import *

app = Flask(__name__)

@app.route('/api/data', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # Handle POST request
        data = request.form.get('data')
        return f'You submitted: {data}'
    else:
        # Handle GET request
        data = {'message': 'Hello from Flask!'}
        return jsonify(data)



def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()