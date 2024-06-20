from datetime import datetime
import json

class Task:
    def __init__(self, title, description, due_date, status, task_id=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.id = task_id

    def __str__(self):
        return f"ID: {self.id}\nTitle: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date}\nStatus: {self.status}"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        # Assign a new ID if the 'id' key is missing
        task_id = data.get('id')
        return Task(data['title'], data['description'], data['due_date'], data['status'], task_id)


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, task):
        if task.id is None:
            task.id = self.next_id
            self.next_id += 1
        self.tasks.append(task)

    def view_tasks(self):
        return self.tasks

    def update_task(self, task_id, **kwargs):
        task = self._find_task_by_id(task_id)
        if task:
            task.title = kwargs.get('title', task.title)
            task.description = kwargs.get('description', task.description)
            task.due_date = kwargs.get('due_date', task.due_date)
            task.status = kwargs.get('status', task.status)
            return True
        return False

    def delete_task(self, task_id):
        task = self._find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def save_tasks(self, filename):
        with open(filename, 'w') as f:
            tasks_data = [task.to_dict() for task in self.tasks]
            json.dump(tasks_data, f)

    def load_tasks(self, filename):
        try:
            with open(filename, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(data) for data in tasks_data]
                if self.tasks:
                    max_id = max((task.id for task in self.tasks if task.id is not None), default=0)
                    self.next_id = max_id + 1
                else:
                    self.next_id = 1
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {filename}.")

    def _find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
