from datetime import timedelta

import pytest

from tests.factories import TransactionFactory, BudgetFactory, CategoryFactory

pytestmark = pytest.mark.django_db

def test_anon_client_get(anon_client):
    response = anon_client.get('/api/transactions/')

    assert response.status_code == 401

def test_client_get(api_client):
    response = api_client.get('/api/transactions/')

    assert response.status_code == 200

def test_transaction_list_returns_only_own_transactions(user, other_user, api_client):
    user_transaction = TransactionFactory(user=user)
    TransactionFactory(user=other_user)
    response = api_client.get('/api/transactions/')

    assert response.data[0]['id'] == str(user_transaction.id)
    assert len(response.data) == 1

def test_create_transaction(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user, type='income')
    response = api_client.post('/api/transactions/', {'budget': str(budget.id), 'category': category.id, 'amount': 1000.00, 'type': 'income', 'date': budget.date_from}, format='json')

    assert response.status_code == 201
    assert response.data['budget'] == budget.id

def test_create_transaction_with_other_users_budget(api_client, user, other_user):
    budget = BudgetFactory(user=other_user)
    category = CategoryFactory(user=user)
    response = api_client.post('/api/transactions/', {'budget': str(budget.id), 'category': category.id, 'amount': 1000.00, 'type': 'income', 'date': budget.date_from}, format='json')

    assert response.status_code == 400

def test_create_transaction_with_other_users_category(api_client, user, other_user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=other_user)
    response = api_client.post('/api/transactions/', {'budget': str(budget.id), 'category': category.id, 'amount': 1000.00, 'type': 'income', 'date': budget.date_from}, format='json')

    assert response.status_code == 400

def test_anon_client_create_transaction(anon_client):
    response = anon_client.post('/api/transactions/')

    assert response.status_code == 401

@pytest.mark.parametrize("amount", [0, -2, -100])
def test_create_transaction_with_negative_amount(api_client, user, amount):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    response = api_client.post('/api/transactions/', {'budget': str(budget.id), 'category': category.id, 'amount': amount, 'type': 'income', 'date': budget.date_from}, format='json')

    assert response.status_code == 400

def test_create_transaction_with_incorrect_date(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    response = api_client.post('/api/transactions/', {'budget': str(budget.id), 'category': category.id, 'amount': 1000.00, 'type': 'income', 'date': budget.date_to + timedelta(days=30)}, format='json')

    assert response.status_code == 400

def test_create_transaction_with_missing_field(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    response = api_client.post('/api/transactions/', {'budget': str(budget.id), 'category': category.id, 'type': 'income', 'date': budget.date_to}, format='json')

    assert response.status_code == 400

@pytest.mark.parametrize("transaction_type, category_type", [
    ('saving_deposit', 'income'),
    ('income', 'saving'),
])
def test_create_transaction_with_incompatible_type_and_category(api_client, user, transaction_type, category_type):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user, type=category_type)
    response = api_client.post('/api/transactions/', {'budget': str(budget.id), 'category': category.id, 'type': transaction_type, 'date': budget.date_to}, format='json')

    assert response.status_code == 400

def test_get_detail(api_client, user):
    transaction = TransactionFactory(user=user)
    response = api_client.get(f'/api/transactions/{transaction.id}/')

    assert response.status_code == 200

def test_cannot_get_other_users_transaction(api_client, other_user):
    transaction = TransactionFactory(user=other_user)
    response = api_client.get(f'/api/transactions/{transaction.id}/')

    assert response.status_code == 404

def test_partial_edit(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user, type='saving')
    transaction = TransactionFactory(user=user, budget=budget, category=category, type='saving_deposit')
    response = api_client.put(f'/api/transactions/{transaction.id}/', {'amount': 1200.00}, format='json')

    assert response.status_code == 200
    assert response.data['amount'] == '1200.00'

def test_partial_edit_other_transaction(api_client, other_user):
    budget = BudgetFactory(user=other_user)
    category = CategoryFactory(user=other_user)
    transaction = TransactionFactory(budget=budget, category=category)
    response = api_client.put(f'/api/transactions/{transaction.id}/', {'amount': 1200.00}, format='json')

    assert response.status_code == 404

def test_delete(api_client, user):
    transaction = TransactionFactory(user=user)
    response = api_client.delete(f'/api/transactions/{transaction.id}/')

    assert response.status_code == 204

def test_delete_other_users_transaction(api_client, other_user):
    transaction = TransactionFactory(user=other_user)
    response = api_client.delete(f'/api/transactions/{transaction.id}/')

    assert response.status_code == 404

