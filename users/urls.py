from django.urls import path

import users.views as views

urlpatterns = [
    path('login', views.login, name='login'),
    path('getData', views.getData, name='getData'),
    path('getProducts', views.getProducts, name='getProducts'),
]
