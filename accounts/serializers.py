from django.contrib.auth.models import User
from rest_framework import serializers

from .models import MembershipTier, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Read-only representation of a user's profile and membership status.
    Nested inside UserDetailSerializer -- never used as a standalone endpoint.
    """

    class Meta:
        model = UserProfile
        fields = ["membership_tier", "is_premium", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles new user registration.

    Accepts an optional membership_tier field. When omitted, the account
    defaults to Basic. Both password fields are write-only and never
    returned in any response.
    """

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, label="Confirm password")
    membership_tier = serializers.ChoiceField(
        choices=MembershipTier.choices,
        default=MembershipTier.BASIC,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm", "membership_tier"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Password fields do not match."}
            )
        return attrs

    def create(self, validated_data):
        tier = validated_data.pop("membership_tier", MembershipTier.BASIC)
        validated_data.pop("password_confirm")

        user = User.objects.create_user(**validated_data)

        # The post_save signal creates the profile automatically.
        # We only need to set the tier if it differs from the default.
        if tier != MembershipTier.BASIC:
            user.profile.membership_tier = tier
            user.profile.save()

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Full representation of an authenticated user, including profile data.
    Used by the registration response and the /me/ endpoint.
    """

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class UpgradeMembershipSerializer(serializers.ModelSerializer):
    """
    Partial update serializer used exclusively by the upgrade endpoint.
    Restricted to the membership_tier field to prevent mass assignment.
    """

    class Meta:
        model = UserProfile
        fields = ["membership_tier"]