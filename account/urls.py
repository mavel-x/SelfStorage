from django.urls import path
from . import views


urlpatterns = [
    path('', views.AccountView.as_view(), name='account'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('change/', views.AccountChangeView.as_view(), name='account_change')
]
