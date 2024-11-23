from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'), 
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('notes/<int:note_id>/', views.view_note, name='view_note'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/search/', views.search_notes, name='search_notes'),
    path('logout/', views.user_logout, name='logout'),

]