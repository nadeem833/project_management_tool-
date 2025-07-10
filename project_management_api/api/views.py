from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import User, Project, ProjectMember, Task, Comment
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    ProjectSerializer, TaskSerializer, CommentSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['register', 'login']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        # Automatically add owner as admin member
        ProjectMember.objects.create(
            project=project,
            user=self.request.user,
            role='Admin'
        )
    
    def get_queryset(self):
        # Users can only see projects they own or are members of
        return Project.objects.filter(
            models.Q(owner=self.request.user) |
            models.Q(members__user=self.request.user)
        ).distinct()
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        project_id = self.request.data.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(project=project)
    
    def get_queryset(self):
        # Users can only see tasks from projects they have access to
        return Task.objects.filter(
            project__in=Project.objects.filter(
                models.Q(owner=self.request.user) |
                models.Q(members__user=self.request.user)
            )
        ).distinct()
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        task = self.get_object()
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        task_id = self.request.data.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        serializer.save(user=self.request.user, task=task)
    
    def get_queryset(self):
        # Users can only see comments from tasks they have access to
        return Comment.objects.filter(
            task__project__in=Project.objects.filter(
                models.Q(owner=self.request.user) |
                models.Q(members__user=self.request.user)
            )
        ).distinct()
