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

class ClientTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_authentication_required(self):
        response = self.client.get("/todo/")
        self.assertRedirects(response, "/accounts/login/?next=/todo/")

    def test_login_view(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302) # Redirect to success page
        # Verify the user is authenticated in the session
        self.assertTrue('_auth_user_id' in self.client.session)
        self.client.logout()

    def test_index(self):
        self.client.force_login(self.user)
        response = self.client.get("/todo/")
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_todo_create(self):
        self.client.force_login(self.user)
        response = self.client.get("/todo/create/")
        self.assertEqual(response.status_code, 200)
        self.client.logout()
