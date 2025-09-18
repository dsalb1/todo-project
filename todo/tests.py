from django.test import Client, TestCase

from django.contrib.auth.models import User
from todo.models import ToDo
# Create your tests here.

class ToDoTestCase(TestCase):
    def setUp(self):
        #create test users
        User.objects.create(username="user1", password="secret", email="user1@gmail.com")
        User.objects.create(username="user2", email="user2@gmail.com")

        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")

        #create test todos
        ToDo.objects.create(title="new todo 1", text="some todo text", author=user1)
        ToDo.objects.create(title="new todo 2", text="some more todo text", author=user2)
    
    def test_todo_creation(self):
        # query users and todos
        todo1 = ToDo.objects.get(title="new todo 1")
        todo2 = ToDo.objects.get(title="new todo 2")
        user2 = User.objects.get(username="user2")
        
        #assert relationship between todo and author
        self.assertEqual(todo1.author.username, "user1")
        #assert lookup ref between user and todos that they own
        self.assertEqual(user2.todos.first(), todo2)

# class ClientTest(TestCase):
#     def test_authentication(self):
#         client = Client()
#         response = client.get("/todo/")
#         self.assertRedirects(response, "/accounts/login/?next=/todo/")

#     def test_index(self):
#         client = Client()
#         response = client.get("/todo/")
#         print(response)
#         self.assertEqual(response.status_code, 200)

#     def test_create(self):
#         client = Client()
#         response = client.get("/todo/create/")
#         self.assertEqual(response.status_code, 200)