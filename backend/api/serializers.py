from django.contrib.auth.models import User
from .models import Profile, FoodLog, CustomMeal
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = { "password": {"write_only": True} }
    
    def validate_password(self, value):
        if value:
            try:
                validate_password(value)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class UpdateUserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ["username", "old_password", "new_password"]
        extra_kwargs = {
            "username": {"required": False}
        }

    def validate(self, data):
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if new_password and not old_password:
            raise serializers.ValidationError({"old_password": "This field is required to change the password."})

        if old_password and not new_password:
            raise serializers.ValidationError({"new_password": "New password is required to change the old password."})

        return data

    def validate_old_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        if value:
            try:
                validate_password(value)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)

        if "new_password" in validated_data:
            instance.set_password(validated_data["new_password"])

        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "age", "weight", "height", "activity_level", "dietary_preferences", "allergies", "fitness_goal"]
        extra_kwargs = { "user": { "read_only": True } }
    
    def create(self, validated_data):
        user = self.context["request"].user

        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a profile.")
        validated_data["user"] = user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return {"message": "Profile deleted successfully"}
    

class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = ["id", "food_name", "calories", "meal_time"]
        read_only_fields = ["id", "meal_time"]

class CustomMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMeal
        fields = ["id", "meal_name", "calories", "created_at"]
        