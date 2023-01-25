from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('explore', views.explore, name='explore'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('upload', views.upload, name='upload'),
    path('like_post', views.like_post, name='like_post'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
]
