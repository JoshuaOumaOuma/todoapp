from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('register/',views.register,name="register"),
    path('home/',views.home,name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('Delete/<str:name>/',views.Delete,name="Delete"),
    path('update/<str:name>/',views.update,name="update"),
]
