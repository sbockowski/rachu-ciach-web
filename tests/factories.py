import factory
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from apps.core.models import User
from apps.budgets.models import Category, Budget, BudgetPlan
from apps.transactions.models import Transaction
from apps.savings.models import SavingsSnapshot
from faker import Faker
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = factory.LazyFunction(lambda: make_password('pi3.1415'))


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    type = factory.Iterator(Category.Type)


class BudgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Budget

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    date_from = factory.Faker('future_date', end_date="+30d")
    date_to = factory.LazyAttribute(lambda o: o.date_from + timedelta(days=30))


class BudgetPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BudgetPlan

    budget = factory.SubFactory(BudgetFactory)
    category = factory.SubFactory(CategoryFactory)
    planned_amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    budget = factory.LazyAttribute(lambda o: BudgetFactory(user=o.user))
    category = factory.LazyAttribute(lambda o: CategoryFactory(user=o.user))
    amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    type = factory.Iterator(Transaction.Type)
    date = factory.LazyAttribute(lambda o: fake.date_between(start_date=o.budget.date_from, end_date=o.budget.date_to))


class SavingsSnapshotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SavingsSnapshot

    user = factory.SubFactory(UserFactory)
    category = factory.LazyAttribute(lambda o: CategoryFactory(user=o.user))
    balance = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    snapshot_date = factory.LazyAttribute(lambda o: fake.date_between(start_date=o.budget.date_from, end_date=o.budget.date_to))
