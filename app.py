from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for tasks
tasks = {}
task_id_counter = 1

@app.route('/tasks', methods=['POST'])
def add_task():
    global task_id_counter
    data = request.get_json()
    task = {
        'id': task_id_counter,
        'title': data.get('title'),
        'description': data.get('description'),
        'summary': data.get('summary', ''),
        'reminder': data.get('reminder', '')
    }
    tasks[task_id_counter] = task
    task_id_counter += 1
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    task = tasks[task_id]
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['summary'] = data.get('summary', task['summary'])
    task['reminder'] = data.get('reminder', task['reminder'])
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(tasks[task_id])

@app.route('/tasks', methods=['GET'])
def list_tasks():
    return jsonify(list(tasks.values()))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
