from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    activity_level = models.CharField(
        max_length=50,
        choices=[
            ("sedentary", "Sedentary"),
            ("light", "Light Activity"),
            ("moderate", "Moderate Activity"),
            ("active", "Highly Active")
        ],
        default="sedentary"
    )
    dietary_preferences = models.TextField(blank=True, null=True, help_text="E.g. Vegan, Keto, Gluten-Free")
    allergies = models.TextField(blank=True, null=True, help_text="E.g. Peanuts, Dairy")
    fitness_goal = models.CharField(
        max_length=50,
        choices= [
            ("weight loss", "Weight Loss"),
            ("muscle gain", "Muscle Gain"),
            ("maintenance", "Maintenance")
        ],
        default="maintenance"
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"