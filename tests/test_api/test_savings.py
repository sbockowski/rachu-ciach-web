from datetime import date, timedelta

import pytest

from tests.factories import SavingsSnapshotFactory, CategoryFactory

pytestmark = pytest.mark.django_db

def test_anon_client_get(anon_client):
    response = anon_client.get('/api/savings/')

    assert response.status_code == 401

def test_client_get(api_client):
    response = api_client.get('/api/savings/')

    assert response.status_code == 200

def test_saving_list_returns_only_own_saving(user, other_user, api_client):
    user_saving = SavingsSnapshotFactory(user=user)
    SavingsSnapshotFactory(user=other_user)
    response = api_client.get('/api/savings/')

    assert response.data[0]['id'] == str(user_saving.id)
    assert len(response.data) == 1

def test_create_saving_snapshot(api_client, user):
    category = CategoryFactory(user=user, type='saving')
    response = api_client.post('/api/savings/', {'category': category.id, 'balance': 1500.00, 'snapshot_date': str(date.today())}, format='json')

    assert response.status_code == 201
    assert response.data['balance'] == '1500.00'

def test_create_saving_snapshot_with_other_users_category(api_client, user, other_user):
    category = CategoryFactory(user=other_user, type='saving')
    response = api_client.post('/api/savings/', {'category': category.id, 'balance': 1500.00, 'snapshot_date': str(date.today())}, format='json')

    assert response.status_code == 400

def test_anon_client_create_saving_snapshot(anon_client):
    response = anon_client.post('/api/savings/')

    assert response.status_code == 401

@pytest.mark.parametrize("balance", [0, -2, -100])
def test_create_saving_snapshot_with_negative_balance(api_client, user, balance):
    category = CategoryFactory(user=user, type='saving')
    response = api_client.post('/api/savings/', {'category': category.id, 'balance': balance, 'snapshot_date': str(date.today())}, format='json')

    assert response.status_code == 400

def test_create_saving_snapshot_with_incorrect_date(api_client, user):
    category = CategoryFactory(user=user, type='saving')
    response = api_client.post('/api/savings/', {'category': category.id, 'balance': 1500.00, 'snapshot_date': str(date.today() + timedelta(days=2))}, format='json')

    assert response.status_code == 400

def test_create_saving_snapshot_with_missing_field(api_client, user):
    category = CategoryFactory(user=user, type='saving')
    response = api_client.post('/api/savings/', {'category': category.id, 'snapshot_date': str(date.today())}, format='json')

    assert response.status_code == 400

@pytest.mark.parametrize("category_type", ['income', 'expense'])
def test_create_saving_snapshot_with_incompatible_category(api_client, user, category_type):
    category = CategoryFactory(user=user, type=category_type)
    response = api_client.post('/api/savings/', {'category': category.id, 'balance': 1500.00, 'snapshot_date': str(date.today())}, format='json')

    assert response.status_code == 400

def test_get_detail(api_client, user):
    saving = SavingsSnapshotFactory(user=user)
    response = api_client.get(f'/api/savings/{saving.id}/')

    assert response.status_code == 200

def test_cannot_get_other_users_saving(api_client, other_user):
    saving = SavingsSnapshotFactory(user=other_user)
    response = api_client.get(f'/api/savings/{saving.id}/')

    assert response.status_code == 404

def test_partial_edit(api_client, user):
    category = CategoryFactory(user=user, type='saving')
    saving = SavingsSnapshotFactory(user=user)
    response = api_client.put(f'/api/savings/{saving.id}/', {'category': category.id, 'balance': 2000.00}, format='json')

    assert response.status_code == 200
    assert response.data['balance'] == '2000.00'

def test_partial_edit_other_saving_snapshot(api_client, other_user):
    category = CategoryFactory(user=other_user, type='saving')
    saving = SavingsSnapshotFactory(user=other_user)
    response = api_client.put(f'/api/savings/{saving.id}/', {'category': category.id, 'balance': 2000.00}, format='json')

    assert response.status_code == 404

def test_delete(api_client, user):
    saving = SavingsSnapshotFactory(user=user)
    response = api_client.delete(f'/api/savings/{saving.id}/')

    assert response.status_code == 204

def test_delete_other_users_saving_snapshot(api_client, other_user):
    saving = SavingsSnapshotFactory(user=other_user)
    response = api_client.delete(f'/api/savings/{saving.id}/')

    assert response.status_code == 404

