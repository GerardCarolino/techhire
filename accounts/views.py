from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, UserDetailSerializer, UpgradeMembershipSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/

    Creates a new user account. No authentication required.

    Request body:
        username        string   Required.
        email           string   Required.
        password        string   Required. Minimum 8 characters.
        password_confirm string  Required. Must match password.
        membership_tier string   Optional. "basic" (default) or "premium".

    Returns the created user's public profile on success (HTTP 201).
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "status": "created",
                "detail": "Account registered successfully.",
                "data": UserDetailSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class MeView(generics.RetrieveAPIView):
    """
    GET /api/accounts/me/

    Returns the authenticated user's account details and membership tier.
    Requires a valid JWT in the Authorization header.
    """

    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpgradeMembershipView(APIView):
    """
    PATCH /api/accounts/upgrade/

    Upgrades the authenticated user's membership tier from Basic to Premium.
    Requires a valid JWT in the Authorization header.

    In production this endpoint should be preceded by payment verification.
    The upgrade itself is idempotent -- calling it on a Premium account
    returns 200 with no changes applied.
    """

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        profile = getattr(request.user, "profile", None)

        if profile is None:
            return Response(
                {"status": "error", "detail": "User profile not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = UpgradeMembershipSerializer(
            profile,
            data={"membership_tier": "premium"},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "status": "success",
                "detail": "Membership upgraded to Premium.",
                "data": {"membership_tier": profile.membership_tier},
            },
            status=status.HTTP_200_OK,
        )