# notes_api/views.py

from api.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import AccountUser

# class RegisterView(CreateAPIView):
#     queryset = AccountUser.objects.all()
#     permission_classes = (AllowAny,)  # Allow anyone to register
#     serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = AccountUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    # templates = "users/signup.html"


class CustomTokenObtainPairView(TokenObtainPairView):
    # This will allow customization of token claims if needed
    pass
