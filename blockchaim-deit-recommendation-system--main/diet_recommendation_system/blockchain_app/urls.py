from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('health_id/', views.health_id, name='health_id'),
    path('diet/', views.diet, name='diet'),
    path('retrieve/', views.retrieve_patient, name='retrieve'),
    path('create_plan/', views.create_plan, name='create_plan'),
    path('generate_plan/', views.generate_plan, name='generate_plan'),
    
]
