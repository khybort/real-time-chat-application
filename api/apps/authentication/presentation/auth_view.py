from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from apps.authentication.presentation.serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer
from apps.shared.dependencies import get_authentication_service

service = get_authentication_service()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            service.register_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = service.login_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            tokens = service.generate_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(APIView):
    """
    Refresh token kullanarak yeni access token oluşturur.
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tokens = service.refresh_access_token(serializer.validated_data["refresh"])
                return Response(tokens, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
