from flask import Flask, request, jsonify
from typing import Callable
from typing import Callable

try:
    from dtypes.stack import Stack
except ModuleNotFoundError:
    from server.dtypes.stack import Stack

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/execute', methods=['POST'])
def execute_stack():
    try:
        data = request.get_json()
        if not data or 'instructions' not in data:
            return jsonify({'error': 'Missing instructions'}), 400

        stack = Stack()

        # Execute instructions
        stack.execute_instructions(data['instructions'])

        response = {
            'status': 'success',
            'final_stack': str(stack),
            'prints': stack.prints,

        }
        print(response)
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    # stack = Stack()
    # instructions = '1 WHILE DUP 10 LT DO DUP PRINT 1 ADD END'
    # stack.execute_instructions(instructions)
    # print(str(stack))
    #
    # conditions = ['DUP', 0, 'LT']
    # body = ['DUP', 'PRINT', '1', 'ADD']
