import pytest

from tests.factories import BudgetFactory

pytestmark = pytest.mark.django_db

def test_anon_client_get(anon_client):
    response = anon_client.get('/api/budgets/')

    assert response.status_code == 401

def test_client_get(api_client):
    response = api_client.get('/api/budgets/')

    assert response.status_code == 200

def test_budget_list_returns_only_own_budgets(user, other_user, api_client):
    user_budget = BudgetFactory(user=user)
    BudgetFactory(user=other_user)

    response = api_client.get('/api/budgets/')

    assert response.data[0]['id'] == str(user_budget.id)
    assert len(response.data) == 1

def test_create_budget(api_client):
    response = api_client.post('/api/budgets/', {'name': 'TestBudget', 'date_from': '2025-03-01', 'date_to': '2025-03-31'}, format='json')

    assert response.status_code == 201
    assert response.data['name'] == 'TestBudget'

def test_anon_client_create_budget(anon_client):
    response = anon_client.post('/api/budgets/', {'name': 'TestBudget', 'date_from': '2025-03-01', 'date_to': '2025-03-31'}, format='json')

    assert response.status_code == 401

def test_create_budget_with_incorrect_dates(api_client):
    response = api_client.post('/api/budgets/', {'name': 'TestBudget', 'date_from': '2025-04-01', 'date_to': '2025-03-31'}, format='json')

    assert response.status_code == 400

def test_create_budget_with_missing_field(api_client):
    response = api_client.post('/api/budgets/', {'name': 'TestBudget', 'date_from': '2025-04-01'}, format='json')

    assert response.status_code == 400

def test_get_detail(api_client, user):
    budget = BudgetFactory(user=user)
    response = api_client.get(f'/api/budgets/{budget.id}/')

    assert response.status_code == 200

def test_cannot_get_other_users_budget(api_client, other_user):
    budget = BudgetFactory(user=other_user)
    response = api_client.get(f'/api/budgets/{budget.id}/')

    assert response.status_code == 404

def test_partial_edit(api_client, user):
    budget = BudgetFactory(user=user)
    response = api_client.put(f'/api/budgets/{budget.id}/', {'name': 'TestBudget', 'date_from': '2025-04-01'}, format='json')

    assert response.status_code == 200
    assert response.data['name'] == 'TestBudget'

def test_partial_edit_other_users_budget(api_client, other_user):
    budget = BudgetFactory(user=other_user)
    response = api_client.put(f'/api/budgets/{budget.id}/', {'name': 'TestBudget', 'date_from': '2025-04-01'}, format='json')

    assert response.status_code == 404

def test_delete(api_client, user):
    budget = BudgetFactory(user=user)
    response = api_client.delete(f'/api/budgets/{budget.id}/')

    assert response.status_code == 204

def test_delete_other_users_budget(api_client, other_user):
    budget = BudgetFactory(user=other_user)
    response = api_client.delete(f'/api/budgets/{budget.id}/')

    assert response.status_code == 404

