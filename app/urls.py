from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('auth/register/', register, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),
    path('create-survey/', create_survey, name='create_survey'),
]
