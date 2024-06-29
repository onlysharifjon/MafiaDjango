from django.urls import path
from .views import *

urlpatterns = [
    path('v1/login/', Login_API.as_view())
]
