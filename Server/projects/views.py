from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Project
from .serializers import ProjectSerializer

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    """项目视图集"""
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """获取项目列表"""
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(collaborators=user) | Q(is_public=True)
        ).distinct()

    def perform_create(self, serializer):
        """创建项目"""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """获取权限"""
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def check_object_permissions(self, request, obj):
        """检查对象权限"""
        if obj.owner == request.user or request.user in obj.collaborators.all():
            return True
        if obj.is_public and self.action in ['retrieve']:
            return True
        return super().check_object_permissions(request, obj)

    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        """添加协作者"""
        project = self.get_object()
        if project.owner != request.user:
            return Response(
                {"detail": "只有项目所有者才能添加协作者"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {"detail": "请提供用户ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            if user == project.owner:
                return Response(
                    {"detail": "不能将项目所有者添加为协作者"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            project.collaborators.add(user)
            return Response(ProjectSerializer(project).data)
        except User.DoesNotExist:
            return Response(
                {"detail": "用户不存在"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_collaborator(self, request, pk=None):
        """移除协作者"""
        project = self.get_object()
        if project.owner != request.user:
            return Response(
                {"detail": "只有项目所有者才能移除协作者"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {"detail": "请提供用户ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            project.collaborators.remove(user)
            return Response(ProjectSerializer(project).data)
        except User.DoesNotExist:
            return Response(
                {"detail": "用户不存在"},
                status=status.HTTP_404_NOT_FOUND
            )
