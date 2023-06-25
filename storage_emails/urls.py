from django.urls import path

from . import views

urlpatterns = [
    path('unlock-box/', views.unlock_box, name='unlock_box'),
]
