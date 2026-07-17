from django.urls import path

from . import views

urlpatterns = [
    # Students 

    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),

    # Admin

    path('manage/', views.course_manage_list, name='course_manage_list'),
    path('manage/create/', views.course_create, name='course_create'),
    path('manage/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('manage/<int:pk>/delete/', views.course_delete, name='course_delete'),
]