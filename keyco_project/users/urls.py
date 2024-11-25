from django.urls import path
from .views import signup_view, login_view, logout_view, people_view, dashboard_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('people/', people_view, name='people'),
    path('', dashboard_view, name='dashboard'), 
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # Routes for 'app'
]
