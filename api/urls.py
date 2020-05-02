from django.urls import include, path
from . import views

urlpatterns = [
    path('welcome', views.welcome),
    path('addpicture/', views.FileUploadView.as_view()),
    path('addalbum/', views.add_album),
    path('get_albums/', views.get_albums),
    path('get_pictures/', views.get_pictures),
    path('register/', views.create_auth),
    path('album/<int:pk>', views.album_detail),
    path('all_albums/', views.get_public_albums),
    path('show_album/<int:pk>', views.get_public_album),



]
