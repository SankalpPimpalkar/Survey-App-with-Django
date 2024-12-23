from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('auth/register/', register, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),

    path('create-survey/', create_survey, name='create_survey'),
    path('survey/<survey_id>/add-question/', add_question, name='add_question'),

    path('survey/<survey_id>/', get_survey_by_id, name='get_survey_by_id'), 
    path('survey/<survey_id>/delete/', delete_survey_by_id, name='delete_survey_by_id'), 
]
