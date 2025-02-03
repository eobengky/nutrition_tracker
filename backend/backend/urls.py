from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView, CreateProfileView, UpdateProfileView, DeleteProfileView, RetrieveProfileView, DeleteUserView, UpdateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/user/update/", UpdateUserView.as_view(), name="update-user"),
    path("api/user/delete/", DeleteUserView.as_view(), name="delete-user"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),

    # Profile endpoints
    path("api/user/profile/", RetrieveProfileView.as_view(), name="get-profile"),
    path("api/user/profile/create/", CreateProfileView.as_view(), name="create-profile"),
    path("api/user/profile/update/", UpdateProfileView.as_view(), name="update-profile"),
    path("api/user/profile/delete/", DeleteProfileView.as_view(), name="delete-profile"),
]

