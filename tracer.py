from datetime import datetime
from enum import Enum
import json
import shlex

class Status(Enum):
    TODO = 1
    PROGRESS= 2
    DONE = 3
class Task:
    def __init__(self, description):
        self.id = None
        self.description = description
        self.status = Status.TODO.value
        self.createAt = str(datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.updateAt = str(datetime.now().strftime("%d/%m/%Y %H:%M"))

    def __str__(self):
        return f"id: {self.id}, description: {self.description}, status: {self.status}, create at: {self.createAt}, update at: {self.updateAt}"
    
    def get_dict(self):
        dict_obj = {
            'id' :self.id,
            'description':self.description,
            'status': self.status,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return dict_obj
    
    @staticmethod
    def help():
        return ("""
        Wellcome to task-cli, to use insert the commands: 
        -----------------------------------------------------
        to add a new task use - add "task message"      
        to update a task message - update <id> "task message"
        to update a task status - <options> <id>
                - options: mark-in-progress; mark-done
        to delete a task - delete <id>
        to list the all tasks - list
        to list the tasks by status- list <options>
                - options: todo; in-progress, done
        to stop the programm use - exit
""")

def main():
    user_escape = False
    while user_escape != True:
        try:
            command_line = shlex.split(input("task-cli "))
            command = command_line[0].lower()
            if command == 'add':
                create_task(command_line[1])
            elif command == 'update':
                id = int(command_line[1])
                description = command_line[2]
                update_task(id, description)
            elif command == 'delete':
                id = int(command_line[1])
                delete_task(id)
            elif command == 'mark-in-progress' or command == 'mark-done':
                id = int(command_line[1])
                update_status(id, command)
            elif command == 'list':
                if len(command_line) > 1:
                    list_tasks(command_line[1])
                else:
                    list_tasks()
            elif command == 'help':
                print(Task.help())
    
            elif command == 'exit':
                print("Exiting task-cli. Goodbye!")
                user_escape = True
            else:
                print(Task.help()) 
            
        except ValueError:
            print(Task.help())

def create_task(task_description: str):
    if not task_description.strip():
        print("Error: Task description cannot be empty!")
        return
    
    new_task = Task(task_description)
    tasks = read_file()

    if len(tasks) == 0:
        counter_id = 1
    else:
        counter_id = tasks[-1]['id'] + 1
    new_task.id = counter_id  
    tasks.append(new_task.get_dict())
    write_file(tasks)
    print(f"Task added successfully (ID: {len(tasks)})\n")

def update_task(id, task_description):
    tasks = read_file()
    task = next((task for task in tasks if task['id'] == id), None)
    if not task:
        print(f"Task with ID {id} does not exist.")
        return
    
    task['description'] = task_description
    task['updateAt'] = str(datetime.now().strftime("%d/%m/%Y %H:%M"))

    write_file(tasks)
    print(f"Task updated\n")

def delete_task(id):
    tasks = read_file()
    task_to_delete = next((task for task in tasks if task['id'] == id), None)
    if not task_to_delete:
        print(f"Task with ID {id} does not exist.")
        return
    
    tasks.remove(task_to_delete)
    write_file(tasks)
    print(f"Task ID {id} deleted successfully.")


def update_status(id, status):
    tasks = read_file()
    task = next((task for task in tasks if task['id'] == id), None)  # Localiza a tarefa pelo ID
    if not task:
        print(f"Task with ID {id} does not exist.")
        return

    if status == 'mark-in-progress':
        task['status'] = Status.PROGRESS.value
    elif status == 'mark-done':
        task['status'] = Status.DONE.value
    else:
        print("Invalid status. Use 'mark-in-progress' or 'mark-done'.")
        return
    
    task['updateAt'] = datetime.now().strftime("%d/%m/%Y %H:%M")

    write_file(tasks)  # Salva a lista atualizada
    print(f"Task ID {id} updated successfully.")

def list_tasks(status=None):
    tasks = read_file()
    if not status:
        for task in tasks:
            print(task)
    if status:
        search = 0
        if status == 'done':
            search = Status.DONE.value
        elif status == 'todo':
            search = Status.TODO.value
        elif status == 'in-progress':
            search = Status.PROGRESS.value
        else:
            print('Status invalid, try todo, done or in-progress')
            return
        for task in tasks:
            if task['status'] == search:
                print(task)
def read_file():
    try:
        with open('task_control.json', 'r') as file:
            tasks_json = file.read()
        tasks = json.loads(tasks_json)
    except FileNotFoundError:
        tasks = []
    return tasks

def write_file(tasks):
    with open('task_control.json', 'w') as file:
        file.write(json.dumps(tasks, indent=4, ensure_ascii=False))
        
if __name__ == "__main__":
    main()