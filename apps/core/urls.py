from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm
from apps.budgets.views.ui import BudgetsListView

urlpatterns = [
    path('register/', views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(
        template_name="login.html",
        authentication_form=CustomLoginForm,
        redirect_authenticated_user=True
    ), name="login"),
    path('dashboard/', BudgetsListView.as_view(template_name='dashboard.html'), name="dashboard"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
]
