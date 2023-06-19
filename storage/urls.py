from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('boxes/', views.BoxesViews.as_view(), name='boxes'),
]