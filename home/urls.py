from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('projects/', views.projects_list, name='projects_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('chat-api/', views.chat_api, name='chat_api'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/projects/', views.manage_projects, name='dashboard_projects'),
    path('dashboard/projects/<int:pk>/edit/', views.edit_project, name='dashboard_project_edit'),
    path('dashboard/projects/<int:pk>/delete/', views.delete_project, name='dashboard_project_delete'),
    path('dashboard/skills/', views.manage_skills, name='dashboard_skills'),
    path('dashboard/skills/<int:pk>/edit/', views.edit_skill, name='dashboard_skill_edit'),
    path('dashboard/skills/<int:pk>/delete/', views.delete_skill, name='dashboard_skill_delete'),
    path('dashboard/settings/', views.site_settings, name='dashboard_settings'),
]
