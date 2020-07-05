from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search),
    path('search/<str:topic>', views.search, name="search"),
    path('wiki/<str:subject>', views.wiki, name = "wiki"),
    path('createNewPage/', views.createNewPage, name= "newPage"),
    path('index/', views.index, name='pageCreated'),
    path('error/', views.index, name='errorPage'),
    path('editPage/<str:subject>', views.editPage, name="edit"),
    path('randomPage/', views.randomPage, name="random")
    
]
