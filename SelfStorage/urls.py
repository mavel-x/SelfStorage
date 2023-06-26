from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from account.views import index_redirect

admin.site.site_header = "SelfStorage"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('storage.urls')),
    path('account/', include('account.urls')),
    path('email/', include('storage_emails.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/login/', index_redirect, name='index-redirect')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
