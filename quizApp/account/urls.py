from django.urls import path
from . import views
urlpatterns = [
    path('' , views.home , name="home"),
    path('register/',views.register , name="register"),
    path('leaderboard/' , views.leaderboard , name="leaderboard"),
    path('signin/' , views.signin , name="signin"),
    path('profile/<str:username>/' , views.profile , name="profile"),
    path('editprofile/',views.editprofile , name='editprofile'),
    path('signout/',views.signout ,name="signout"),
    path('delete/', views.deleteprofile , name="delete")


]