
from django.urls import path
from . import views

urlpatterns = [

    path('',views.login_auth, name="login"),
    path('register/',views.register, name="register"),
    path('success/',views.success, name="success"),
    path('token/',views.token, name="token"),
    path('verify/<auth_token>/',views.verify, name="verify"),
    path('error/',views.error, name="error"),
    path('home/',views.home, name="home"),
    
    
]
