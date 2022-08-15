from typing import List

from django.urls import path
from . import views


urlpatterns: List = [
    path('', views.dashboard_view, name='items.dashboard'),
    path('delete/<pk>/', views.ItemDeleteView.as_view(), name='items.delete'),
    path('update/', views.update_prices, name='items.update-prices'),
]