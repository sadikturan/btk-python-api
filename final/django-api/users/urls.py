from django.urls import path
from .views import SignUpView, LoginView, CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, AdminUserListView, AdminUserDetailView

urlpatterns = [
    path('signup', SignUpView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name="login"),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', CustomTokenVerifyView.as_view(), name='token_verify'),
    path("admin/users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),
]
