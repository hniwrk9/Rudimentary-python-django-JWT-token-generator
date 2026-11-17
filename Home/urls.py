from django.urls import path
from .views import index, login, logout

urlpatterns = [
    path('', index.as_view(), name="homepage"),
    path('login/', login.as_view(), name="login"),
    path('logout/', logout, name="logout" )
]