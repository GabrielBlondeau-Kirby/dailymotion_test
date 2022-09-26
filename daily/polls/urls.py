from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('create_user', views.create_user, name='create_user'),
    path('verify_user', views.verify_user, name='verify_user'),
    path('refresh', views.refresh_token, name='refresh'),

    # Test
    path('', views.index, name='index'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
