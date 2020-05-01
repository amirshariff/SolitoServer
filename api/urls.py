from django.urls import include, path
from . import views

urlpatterns = [
  path('welcome', views.welcome),
  path('addpicture/', views.FileUploadView.as_view()),
  path('addalbum/', views.add_album),
  path('get_albums/', views.get_albums),
  path('get_pictures/', views.get_pictures)

]
