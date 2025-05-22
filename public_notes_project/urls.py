from django.contrib import admin
from django.urls import path, include
from notes.views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('notes/', include('notes.urls')),
    path('', include('notes.urls')),
]
