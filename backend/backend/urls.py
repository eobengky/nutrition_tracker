from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView, CreateProfileView, UpdateProfileView, DeleteProfileView, RetrieveProfileView, DeleteUserView, UpdateUserView, FoodLogCreateView, FoodLogDeleteView, FoodLogListView, FoodLogUpdateView, CustomMealCreateView, CustomMealUpdateView, CustomMealDeleteView, CustomMealListView, MealRecommendations
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

    # Foodlog enpoints
    path("api/food/log/", FoodLogCreateView.as_view(), name="food-log"),
    path("api/food/log/<int:pk>/update/", FoodLogUpdateView.as_view(), name="food-log-update"),
    path("api/food/logs/", FoodLogListView.as_view(), name="list-food-item"),
    path("api/food/log/<int:pk>/", FoodLogDeleteView.as_view(), name="delete-food-log"),

    # Meal recommendation and custom
    path("api/meal/recommendations/", MealRecommendations.as_view(), name="meal-recommendations"),
    path("api/meal/custom/", CustomMealCreateView.as_view(), name="custom-meal-create"),
    path("api/meal/custom/<int:pk>/update", CustomMealUpdateView.as_view(), name="custom-meal-update"),
    path("api/meal/customs/", CustomMealListView.as_view(), name="custom-meal-list"),
    path("api/meal/custom/<int:pk>/", CustomMealDeleteView.as_view(), name="custom-meal-delete")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
