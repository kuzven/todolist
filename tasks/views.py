from rest_framework.viewsets import ModelViewSet
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
