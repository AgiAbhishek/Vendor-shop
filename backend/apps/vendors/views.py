from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    """
    POST /api/auth/register/  ->  {username, email, password}
    Public endpoint.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "Vendor registered successfully.",
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Extra safety if DB uniqueness triggers
            return Response(
                {"detail": "Username or email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
