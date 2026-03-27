from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserDetailSerializer, UpgradeMembershipSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    Register a new user. Pass membership_tier as "basic" or "premium".
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
                "message": "Registration successful.",
                "user": UserDetailSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class MeView(generics.RetrieveAPIView):
    """
    GET /api/accounts/me/
    Returns the currently authenticated user's details and membership tier.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpgradeMembershipView(APIView):
    """
    PATCH /api/accounts/upgrade/
    Upgrade the authenticated user's membership to Premium.
    In production this would be behind a payment gateway.
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        profile = request.user.profile
        serializer = UpgradeMembershipSerializer(
            profile, data={"membership_tier": "premium"}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "🎉 Upgrade successful! You now have Premium access.",
                "membership_tier": profile.membership_tier,
            }
        )
