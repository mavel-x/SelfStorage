from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('boxes/', views.BoxesViews.as_view(), name='boxes'),
    path('lead/', views.LeadViews.as_view(), name='lead'),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]