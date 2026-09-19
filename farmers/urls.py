from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('farmers/', views.farmer_list, name='farmer_list'),
    path('farmers/add/', views.farmer_create, name='farmer_create'),
    path('farmers/edit/<int:id>/', views.farmer_update, name='farmer_update'),
    path('farmers/delete/<int:id>/', views.farmer_delete, name='farmer_delete'),

     # Authentication
    path('register/', views.register_farmer, name='register_farmer'),
    path('login/', views.login_farmer, name='login_farmer'),
    path('logout/', views.logout_farmer, name='logout_farmer'),

    # Dashboard
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
]   