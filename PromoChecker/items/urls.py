from typing import List

from django.urls import path
from . import views


urlpatterns: List = [
    path('', views.dashboard_view, name='items.dashboard'),
    
    path('delete/<pk>/', views.ItemDeleteView.as_view(), name='items.delete'),
    path('update/', views.update_prices, name='items.update-prices'),
    
    path('login/', views.login_view, name='items.login'),
    path('logout/', views.logout_view, name='items.logout'),
    path('register/', views.register_view, name='items.register'),
]