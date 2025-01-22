
import unittest
from tracer import create_task, read_file, update_task, update_status, delete_task

class TestTaskCli(unittest.TestCase):
    
    def setup(self):
        with open('task_control.json','w') as file:
            file.write('[]')

    def test_create_task(self):
        create_task("Teste de tarefa")
        tasks = read_file()
        self.assertEqual(tasks[-1]['description'], "Teste de tarefa")
        self.assertEqual(tasks[-1]['status'], 1)

    def test_update_task_description(self):
        tasks = read_file()
        id = tasks[-1]['id']
        update_task(id, 'tarefa atualizada')
        tasks = read_file()
        self.assertEqual(tasks[-1]['description'], "tarefa atualizada")
    
    def test_update_status(self):
        tasks = read_file()
        task_id = tasks[-1]['id']
        update_status(task_id, "mark-in-progress")
        tasks = read_file()
        self.assertEqual(tasks[-1]['status'], 2)

    def test_delete_task(self):
        tasks = read_file()
        before = len(tasks)
        task_id = tasks[-1]['id']
        delete_task(task_id)
        tasks = read_file()
        self.assertGreater(before, len(tasks))
        self.assertEqual(before - 1, len(tasks))

    def test_invalid_task_update(self):
        """Teste para atualização de uma tarefa inexistente."""
        tasks = read_file()
        before = len(tasks)
        update_task(999, "Tarefa inexistente")
        tasks = read_file()
        after = len(tasks)
        self.assertEqual(before, after)
        
if __name__ == '__main__':
    unittest.main()