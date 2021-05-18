from django.urls import path
from instagram import views

urlpatterns = [
    path('code_from_instagram/', views.code_from_instagram),
]
