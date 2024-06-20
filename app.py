from flask import Flask, request, render_template, redirect, url_for, flash
from task_manager import Task, TaskManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
task_manager = TaskManager()

@app.route('/')
def index():
    tasks = task_manager.view_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form['status']
        if not title or not description or not due_date or not status:
            flash('All fields are required!')
            return redirect(url_for('add_task'))
        task = Task(title, description, due_date, status)
        task_manager.add_task(task)
        flash('Task added successfully!')
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = task_manager._find_task_by_id(task_id)
    if not task:
        flash('Task not found!')
        return redirect(url_for('index'))
    if request.method == 'POST':
        task_manager.update_task(task_id, title=request.form['title'], description=request.form['description'], due_date=request.form['due_date'], status=request.form['status'])
        flash('Task updated successfully!')
        return redirect(url_for('index'))
    return render_template('update_task.html', task=task)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    deleted = task_manager.delete_task(task_id)
    if deleted:
        flash('Task deleted successfully!')
    else:
        flash('Task not found!')
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save_tasks():
    filename = 'tasks.json'
    task_manager.save_tasks(filename)
    flash('Tasks saved successfully!')
    return redirect(url_for('index'))

@app.route('/load', methods=['POST'])
def load_tasks():
    filename = 'tasks.json'
    task_manager.load_tasks(filename)
    flash('Tasks loaded successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
