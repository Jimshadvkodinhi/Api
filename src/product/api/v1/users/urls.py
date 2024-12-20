# api/v1/users/urls.py
from django.urls import path
from api.v1.users import views
from api.v1.users.views import *

app_name = "users_api_v1"

urlpatterns = [
    path('signup/', views.sign_up), 
    path('login/', views.login),
    path('user/profile/', user_profile, name='user-profile'),

]
