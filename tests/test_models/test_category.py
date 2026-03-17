import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from apps.budgets.models import Category
from tests.factories import CategoryFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_category_created():
    category = CategoryFactory()
    assert Category.objects.get(id=category.id)

def test_system_categories():
    category = CategoryFactory(is_system=True, user = UserFactory())
    with pytest.raises(ValidationError):
        category.clean()

def test_user_categories():
    category = CategoryFactory(is_system=False, user = None)
    with pytest.raises(ValidationError):
        category.clean()

def test_category_is_unique():
    test_user = UserFactory()
    CategoryFactory(user=test_user, name="Something", type="expense")
    with pytest.raises(IntegrityError):
        CategoryFactory(user=test_user, name="Something", type="expense")
