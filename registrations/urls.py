from django.urls import path

from . import views

urlpatterns = [
    path('', views.registration_list, name='registration_list'),
    path('<int:pk>/update-status/', views.update_registration_status, name='update_registration_status'),
]
