from django.urls import path
from . import views
urlpatterns = [
    path("allquiz/" , views.allquiz , name="allquiz"),
    path('quiz/<int:id>' , views.quiz ,name="quiz"),
    path('search/<str:category_name>/' , views.search , name="search"),
    path('addquiz/' , views.addquiz , name="addquiz")
]
