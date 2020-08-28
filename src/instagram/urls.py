from django.urls import path
from instagram import views

urlpatterns = [
    path('get_code/', views.get_code),
]
