from django.contrib.auth.models import User
from todo.models import ToDo

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    todos = serializers.HyperlinkedRelatedField(many=True, view_name='todo:todo-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'todos']


class ToDoSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = ToDo
        fields = ['id', 'title', 'text', 'author', 'is_completed', 'created_at', 'updated_at']
