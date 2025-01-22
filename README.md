# TASK-CLI

TASK-CLI it's a Command Line interface it has the goal to create, update, delete and list the tasks. 


### How to use
- Add Task
  - add "task message"
- Update Task Message
  - update < id > "new message" 
- Update Task Status
  - update < id > --options
    - options - mark-done; mark-in-progress
- Delete Task
  - delete < id >  
- List All Tasks
  - list 
- List By Status
  - list --options
    - options: todo; in-progress; done 