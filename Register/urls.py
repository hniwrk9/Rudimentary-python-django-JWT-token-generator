from django.urls import path
from .views import register, ntoken
from .jwt import generateKeys

urlpatterns = [
    path('register/', register.as_view(), name="register"),
    path('ntoken/', ntoken.as_view(), name="ntoken"),

    # Only uncomment the below line when you want to generate new keys for the JWT or payload encryption/decryption.
    # After enabling this path, you can go to it and it will generate new keys and print them in the server messages/logs
    # path('keygen/', generateKeys.as_view(), name="keygen")


]