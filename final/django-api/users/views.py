from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from .serializer import SignUpSerializer, LoginSerializer, UserAdminSerializer
from .tokens import get_tokens_for_user
from rest_framework.permissions import IsAdminUser

User = get_user_model()

@extend_schema(
    request=TokenObtainPairSerializer,
    responses=TokenObtainPairSerializer,
    tags=['Users']
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(
    request=TokenRefreshSerializer,
    responses=TokenObtainPairSerializer,
    tags=['Users']
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(
    request=TokenVerifySerializer,
    responses=None,
    tags=['Users']
)
class CustomTokenVerifyView(TokenVerifyView):
    pass

@extend_schema(
    summary="Kullanıcı oluştur",
    tags=['Users']
)
class SignUpView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()

        tokens = get_tokens_for_user(user)

        response = {
                "message": "User created successfull",
                "token": tokens,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "role": "admin" if user.is_superuser else "user"
                }
            }
        
        return Response(data=response, status=status.HTTP_201_CREATED)

@extend_schema(
    request=LoginSerializer,
    summary="Uygulamaya giriş",
    tags=['Users']
)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)

            response = {
                "message": "Login successfull",
                "token": tokens,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "role": "admin" if user.is_superuser else "user"
                }
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserAdminSerializer,
    summary="Admin Kullanıcı Listesi",
    tags=['Users']
)
class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    request=UserAdminSerializer,
    summary="Admin Kullanıcı Detayı",
    tags=['Users']
)
class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]



