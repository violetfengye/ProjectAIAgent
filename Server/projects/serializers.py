from rest_framework import serializers
from .models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    """用户基本信息序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar')

class ProjectSerializer(serializers.ModelSerializer):
    """项目序列化器"""
    owner = UserBasicSerializer(read_only=True)
    collaborators = UserBasicSerializer(many=True, read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='owner',
        write_only=True
    )
    collaborator_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='collaborators',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'owner', 'owner_id',
            'collaborators', 'collaborator_ids', 'created_at',
            'updated_at', 'is_public', 'status'
        )
        read_only_fields = ('created_at', 'updated_at')

    def validate_owner_id(self, value):
        """验证项目所有者"""
        request = self.context.get('request')
        if request and request.user != value:
            raise serializers.ValidationError("您不能为其他用户创建项目")
        return value

    def validate_collaborator_ids(self, value):
        """验证项目协作者"""
        request = self.context.get('request')
        if request and request.user in value:
            raise serializers.ValidationError("项目所有者不能同时是协作者")
        return value 