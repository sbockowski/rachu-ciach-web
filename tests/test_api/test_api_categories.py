import pytest

from tests.factories import CategoryFactory

pytestmark = pytest.mark.django_db

def test_anon_client_get(anon_client):
    response = anon_client.get('/api/categories/')

    assert response.status_code == 401

def test_client_get(api_client):
    response = api_client.get('/api/categories/')

    assert response.status_code == 200

def test_category_list_returns_only_own_categories(user, other_user, api_client):
    user_category = CategoryFactory(user=user)
    CategoryFactory(user=other_user)

    response = api_client.get('/api/categories/')

    assert response.data[0]['id'] == user_category.id
    assert len(response.data) == 1

def test_category_list_includes_system_categories(user, api_client):
    CategoryFactory(user=user)
    CategoryFactory(user=None, is_system=True)

    response = api_client.get('/api/categories/')

    assert len(response.data) == 2

def test_create_category(api_client):
    response = api_client.post('/api/categories/', {'name': 'TestCategory', 'type': 'income'}, format='json')

    assert response.status_code == 201
    assert response.data['name'] == 'TestCategory'

def test_create_duplicate_category(api_client):
    api_client.post('/api/categories/', {'name': 'TestCategory', 'type': 'income'}, format='json')
    response = api_client.post('/api/categories/', {'name': 'TestCategory', 'type': 'income'}, format='json')

    assert response.status_code == 400

def test_anon_client_create_category(anon_client):
    response = anon_client.post('/api/categories/', {'name': 'TestCategory', 'type': 'income'}, format='json')

    assert response.status_code == 401

def test_create_category_with_missing_field(api_client):
    response = api_client.post('/api/categories/', {'name': 'TestCategory'}, format='json')

    assert response.status_code == 400

def test_get_detail(api_client, user):
    category = CategoryFactory(user=user)
    response = api_client.get(f'/api/categories/{category.id}/')

    assert response.status_code == 200

def test_get_detail_system_category(api_client):
    system_category = CategoryFactory(user=None, is_system=True)
    response = api_client.get(f'/api/categories/{system_category.id}/')

    assert response.status_code == 200

def test_cannot_get_other_users_category(api_client, other_user):
    category = CategoryFactory(user=other_user)
    response = api_client.get(f'/api/categories/{category.id}/')

    assert response.status_code == 404

def test_partial_edit(api_client, user):
    category = CategoryFactory(user=user)
    response = api_client.put(f'/api/categories/{category.id}/', {'name': 'TestCategory'}, format='json')

    assert response.status_code == 200
    assert response.data['name'] == 'TestCategory'

def test_partial_edit_other_users_category(api_client, other_user):
    category = CategoryFactory(user=other_user)
    response = api_client.put(f'/api/categories/{category.id}/', {'name': 'TestCategory'}, format='json')

    assert response.status_code == 404

def test_partial_edit_other_system_category(api_client):
    category = CategoryFactory(user=None, is_system=True)
    response = api_client.put(f'/api/categories/{category.id}/', {'name': 'TestCategory'}, format='json')

    assert response.status_code == 403

def test_delete(api_client, user):
    category = CategoryFactory(user=user)
    response = api_client.delete(f'/api/categories/{category.id}/')

    assert response.status_code == 204

def test_delete_other_users_category(api_client, other_user):
    category = CategoryFactory(user=other_user)
    response = api_client.delete(f'/api/categories/{category.id}/')

    assert response.status_code == 404

def test_delete_system_category(api_client):
    category = CategoryFactory(user=None, is_system=True)
    response = api_client.delete(f'/api/categories/{category.id}/')

    assert response.status_code == 403

