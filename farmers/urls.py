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
    path('predict/', views.ai_prediction, name='ai_prediction'),

    # Dashboard
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    # Farm Management
path('my-farms/', views.my_farms, name='my_farms'),
# Farm Management
path('my-farms/', views.my_farms, name='my_farms'),
# Farm Management
path('my-farms/', views.my_farms, name='my_farms'),
path('farm/add/', views.farm_create, name='farm_create'),
path(
    'farm/edit/<int:id>/',
    views.farm_update,
    name='farm_update'
),
# Crop Management
path(
    'my-crops/',
    views.my_crops,
    name='my_crops'
),
path(
    'farm/delete/<int:id>/',
    views.farm_delete,
    name='farm_delete'
),
path(
    'farm/add/',
    views.farm_create,
    name='farm_create'
),
path(
    'crop/add/',
    views.crop_create,
    name='crop_create'
),
path(
    'my-crops/',
    views.my_crops,
    name='my_crops'
),
path(
    'crop/delete/<int:id>/',
    views.crop_delete,
    name='crop_delete'
),
path(
    'my-crops/',
    views.my_crops,
    name='my_crops'
),
path(
    'crop/edit/<int:id>/',
    views.crop_update,
    name='crop_update'
),

]   