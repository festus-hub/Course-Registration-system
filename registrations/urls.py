from django.urls import path

from . import views

urlpatterns = [
    path('', views.registration_list, name='registration_list'),
    path('<int:pk>/update-status/', views.update_registration_status, name='update_registration_status'),
    path('<int:pk>/delete/', views.delete_registration, name='delete_registration'),
    path('<int:pk>/view/', views.view_registration, name='view_registration'),
    path('<int:pk>/download-pdf/', views.download_registration_pdf, name='download_registration_pdf'),
    path('<int:pk>/edit/', views.registration_edit, name='registration_edit')
]
