import pytest

from tests.factories import BudgetPlanFactory, BudgetFactory, CategoryFactory

pytestmark = pytest.mark.django_db

def test_anon_client_get(anon_client):
    response = anon_client.get('/api/budget_plans/')

    assert response.status_code == 401

def test_client_get(api_client):
    response = api_client.get('/api/budget_plans/')

    assert response.status_code == 200

def test_budget_list_returns_only_own_budget_plans(user, other_user, api_client):
    user_budget = BudgetFactory(user=user)
    other_user_budget = BudgetFactory(user=other_user)
    user_budget_plan = BudgetPlanFactory(budget=user_budget)
    BudgetPlanFactory(budget=other_user_budget)

    response = api_client.get('/api/budget_plans/')

    assert response.data[0]['id'] == user_budget_plan.id
    assert len(response.data) == 1

def test_create_budget_plan(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    response = api_client.post('/api/budget_plans/', {'budget': str(budget.id), 'category': category.id, 'planned_amount': 1000.00 }, format='json')

    assert response.status_code == 201
    assert response.data['budget'] == budget.id

def test_create_budget_plan_with_other_users_budget(api_client, user, other_user):
    budget = BudgetFactory(user=other_user)
    category = CategoryFactory(user=user)
    response = api_client.post('/api/budget_plans/', {'budget': str(budget.id), 'category': category.id, 'planned_amount': 1000.00 }, format='json')

    assert response.status_code == 400

def test_create_budget_plan_with_other_users_category(api_client, user, other_user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=other_user)
    response = api_client.post('/api/budget_plans/', {'budget': str(budget.id), 'category': category.id, 'planned_amount': 1000.00 }, format='json')

    assert response.status_code == 400

def test_anon_client_create_budget_plan(anon_client):
    response = anon_client.post('/api/budget_plans/')

    assert response.status_code == 401

@pytest.mark.parametrize("amount", [0, -2, -100])
def test_create_budget_plan_with_negative_amount(api_client, user, amount):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    response = api_client.post('/api/budget_plans/', {'budget': str(budget.id), 'category': category.id, 'planned_amount': amount }, format='json')

    assert response.status_code == 400

def test_create_budget_plan_with_missing_field(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    response = api_client.post('/api/budget_plans/', {'budget': str(budget.id), 'category': category.id }, format='json')

    assert response.status_code == 400

def test_create_duplicate(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    BudgetPlanFactory(budget=budget, category=category)
    response = api_client.post('/api/budget_plans/', {'budget': str(budget.id), 'category': category.id, 'planned_amount': 1200.00 }, format='json')

    assert response.status_code == 400

def test_get_detail(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    budget_plan = BudgetPlanFactory(budget=budget, category=category)
    response = api_client.get(f'/api/budget_plans/{budget_plan.id}/')

    assert response.status_code == 200

def test_cannot_get_other_users_budget_plan(api_client, other_user):
    budget = BudgetFactory(user=other_user)
    category = CategoryFactory(user=other_user)
    budget_plan = BudgetPlanFactory(budget=budget, category=category)
    response = api_client.get(f'/api/budget_plans/{budget_plan.id}/')

    assert response.status_code == 404

def test_partial_edit(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    budget_plan = BudgetPlanFactory(budget=budget, category=category)
    response = api_client.put(f'/api/budget_plans/{budget_plan.id}/', {'planned_amount': 1200.00}, format='json')

    assert response.status_code == 200
    assert response.data['planned_amount'] == '1200.00'

def test_partial_edit_other_users_budget(api_client, other_user):
    budget = BudgetFactory(user=other_user)
    category = CategoryFactory(user=other_user)
    budget_plan = BudgetPlanFactory(budget=budget, category=category)
    response = api_client.put(f'/api/budget_plans/{budget_plan.id}/', {'planned_amount': 1200.00}, format='json')

    assert response.status_code == 404

def test_delete(api_client, user):
    budget = BudgetFactory(user=user)
    category = CategoryFactory(user=user)
    budget_plan = BudgetPlanFactory(budget=budget, category=category)
    response = api_client.delete(f'/api/budget_plans/{budget_plan.id}/')

    assert response.status_code == 204

def test_delete_other_users_budget(api_client, other_user):
    budget = BudgetFactory(user=other_user)
    category = CategoryFactory(user=other_user)
    budget_plan = BudgetPlanFactory(budget=budget, category=category)
    response = api_client.delete(f'/api/budget_plans/{budget_plan.id}/')

    assert response.status_code == 404

