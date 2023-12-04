import time

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from database import ToDo
from database import get_db
from settings.utils import get_serializers
from fastapi import status
from main import app
import unittest
import os


class ToDoTestCase(unittest.TestCase):

    def run(self, *args, **kwargs):
        super().run()

    def setUp(self):
        self.client = TestClient(app)
        self.db_session: Session = next(get_db())

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass is called!")
        if hasattr(cls, 'db_session'):
            cls.db_session.close_all()
        time.sleep(1)
        file_path = os.path.abspath('todo.db')

        try:
            os.remove(file_path)
            print(f"База данных {file_path} успешно удалена.")
        except Exception as e:
            print(f"Ошибка при удалении базы данных: {e}")

    def create_todo(self):
        todo = ToDo(title="Test Todo")

        self.db_session.add(todo)
        self.db_session.commit()
        return todo.id

    def test_home(self):
        response = self.client.get('/')
        todos = self.db_session.query(ToDo).all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answer = {'todos': get_serializers(todos)}
        self.assertEqual(response.json(), answer)

    def test_create_todo(self):
        response = self.client.post("/add", data={"title": "Test Todo"})
        answer = {"message": "Todo added successfully"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), answer)

    def test_update_todo(self):
        todo_id = self.create_todo()
        response = self.client.get(f"/update/{todo_id}")
        answer = {"message": "Todo updated successfully"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), answer)

    def test_delete_todo(self):
        todo_id = self.create_todo()
        response = self.client.get(f"/delete/{todo_id}")
        answer = {"message": "Todo deleted successfully"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), answer)


if __name__ == '__main__':
    unittest.main()

