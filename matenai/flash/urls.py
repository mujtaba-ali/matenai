from django.contrib.auth import logout
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name="logout"),
    path('res_register', views.res_register, name='res_register'),
    path('add_menu', views.add_menu, name='add_menu'),
    path('menu', views.menu, name='menu'),
    path('edit_menu', views.edit_menu, name='edit_menu')
]