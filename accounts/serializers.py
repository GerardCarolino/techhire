from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, MembershipTier


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["membership_tier", "is_premium", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class RegisterSerializer(serializers.ModelSerializer):
    """Handles new user registration with optional membership tier."""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")
    membership_tier = serializers.ChoiceField(
        choices=MembershipTier.choices,
        default=MembershipTier.BASIC,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2", "membership_tier"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        tier = validated_data.pop("membership_tier", MembershipTier.BASIC)
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        # Signal auto-creates profile; just update the tier
        user.profile.membership_tier = tier
        user.profile.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Returns full user info including membership status."""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class UpgradeMembershipSerializer(serializers.ModelSerializer):
    """Allows users to upgrade their membership tier."""
    class Meta:
        model = UserProfile
        fields = ["membership_tier"]