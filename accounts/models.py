from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class MembershipTier(models.TextChoices):
    BASIC = "basic", "Basic"
    PREMIUM = "premium", "Premium"


class UserProfile(models.Model):
    """
    Extends Django's built-in User model with TechHire-specific attributes.

    One UserProfile is created automatically for every new User via the
    post_save signal below. Callers should use `getattr(user, "profile", None)`
    rather than direct attribute access to handle the rare case where a profile
    does not yet exist (e.g. legacy accounts created outside the signal).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    membership_tier = models.CharField(
        max_length=10,
        choices=MembershipTier.choices,
        default=MembershipTier.BASIC,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self) -> str:
        return f"{self.user.username} ({self.get_membership_tier_display()})"

    @property
    def is_premium(self) -> bool:
        """Returns True when the user holds an active Premium membership."""
        return self.membership_tier == MembershipTier.PREMIUM


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Ensures every User has exactly one associated UserProfile.

    On creation: builds a new profile with the default Basic tier.
    On update:   creates a profile if one is somehow missing (safety net
                 for accounts created outside the normal registration flow).
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)