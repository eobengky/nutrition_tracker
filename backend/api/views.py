from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, FoodLog, CustomMeal
from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, UpdateUserSerializer, FoodLogSerializer, CustomMealSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import openai
import deepseek
from django.conf import settings

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UpdateUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User details updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class CreateProfileView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if Profile.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("User already has a profile")
        serializer.save(user=self.request.user)

class RetrieveProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class UpdateProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Profile updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteProfileView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message" : "Profile deleted successfully"}, status=status.HTTP_200_OK)
        

class FoodLogCreateView(generics.CreateAPIView):
    serializer_class = FoodLogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    

# Update logs
class FoodLogUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = FoodLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodLog.objects.filter(user=self.request.user)
    

    def get_object(self):
        queryset = self.get_queryset()
        return generics.get_object_or_404(queryset, pk=self.kwargs.get("pk"))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Food log updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodLogListView(generics.ListAPIView):
    serializer_class = FoodLogSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return FoodLog.objects.filter(user=self.request.user)

class FoodLogDeleteView(generics.DestroyAPIView):
    serializer_class = FoodLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodLog.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message" : "Food log entry deleted successfully"}, status=status.HTTP_200_OK)


# For Meal Recommendation
class MealRecommendations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_preference = request.GET.get("diet", "healthy meals")
        
        try:
            # openai.api_key = settings.OPENAI_API_KEY
            # client = openai.OpenAI()
            client = openai.OpenAI(api_key=settings.DEEPSEEK_API_KEY, 
                                base_url="https://api.deepseek.com/v1")
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages = [
                    # {"role" : "system", "content": "You are a helpful nutritionist."},
                    {"role" : "system", "content" : f"Suggest three {user_preference} meals with calorie counts."}]
            )

            meal_suggestions = response.choices[0].message.content

            return Response({"recommendations" : meal_suggestions}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Custom Meals
class CustomMealCreateView(generics.CreateAPIView):
    serializer_class = CustomMealSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class CustomMealUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomMealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomMeal.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        return generics.get_object_or_404(queryset, pk=self.kwargs.get("pk"))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Custom meal updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomMealListView(generics.ListAPIView):
    serializer_class = CustomMealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomMeal.objects.filter(user=self.request.user)

class CustomMealDeleteView(generics.DestroyAPIView):
    serializer_class = CustomMealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomMeal.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({"message" : "Custom meal deleted successfully"}, status=status.HTTP_200_OK),
