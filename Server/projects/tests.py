from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from .models import Project

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    return user

@pytest.fixture
def test_collaborator():
    user = User.objects.create_user(
        username='collaborator',
        email='collaborator@example.com',
        password='testpass123'
    )
    return user

@pytest.fixture
def test_project(test_user):
    project = Project.objects.create(
        name='测试项目',
        description='这是一个测试项目',
        owner=test_user,
        is_public=False,
        status='planning'
    )
    return project

@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.mark.django_db
class TestProjectAPI:
    def test_create_project(self, auth_client):
        url = reverse('project-list')
        data = {
            'name': '新项目',
            'description': '这是一个新项目',
            'is_public': False,
            'status': 'planning'
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Project.objects.count() == 1
        assert Project.objects.get().name == '新项目'

    def test_create_project_missing_required_fields(self, auth_client):
        url = reverse('project-list')
        data = {
            'description': '这是一个新项目'
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_get_project_list(self, auth_client, test_project):
        url = reverse('project-list')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == '测试项目'

    def test_get_project_detail(self, auth_client, test_project):
        url = reverse('project-detail', args=[test_project.id])
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == '测试项目'

    def test_get_nonexistent_project(self, auth_client):
        url = reverse('project-detail', args=[999])
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_project(self, auth_client, test_project):
        url = reverse('project-detail', args=[test_project.id])
        data = {
            'name': '更新后的项目名称',
            'description': '更新后的项目描述',
            'status': 'in_progress'
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == '更新后的项目名称'
        assert response.data['status'] == 'in_progress'

    def test_delete_project(self, auth_client, test_project):
        url = reverse('project-detail', args=[test_project.id])
        data = {'action': 'delete'}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Project.objects.count() == 0

    def test_add_collaborator(self, auth_client, test_project, test_collaborator):
        url = reverse('project-add-collaborator', args=[test_project.id])
        data = {'user_id': test_collaborator.id}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert test_collaborator in test_project.collaborators.all()

    def test_remove_collaborator(self, auth_client, test_project, test_collaborator):
        test_project.collaborators.add(test_collaborator)
        url = reverse('project-remove-collaborator', args=[test_project.id])
        data = {'user_id': test_collaborator.id}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert test_collaborator not in test_project.collaborators.all()

    def test_unauthorized_access(self, api_client, test_project):
        url = reverse('project-detail', args=[test_project.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_owner_access(self, api_client, test_project, test_collaborator):
        api_client.force_authenticate(user=test_collaborator)
        url = reverse('project-detail', args=[test_project.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_public_project_access(self, api_client, test_user, test_project):
        test_project.is_public = True
        test_project.save()
        api_client.force_authenticate(user=test_user)
        url = reverse('project-detail', args=[test_project.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
