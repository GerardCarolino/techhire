from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class MembershipTier(models.TextChoices):
    BASIC = "basic", "Basic"
    PREMIUM = "premium", "Premium"


class UserProfile(models.Model):
    """
    Extends Django's built-in User with TechHire membership tier.
    Auto-created when a new User is registered.
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

    def __str__(self):
        return f"{self.user.username} — {self.get_membership_tier_display()}"

    @property
    def is_premium(self) -> bool:
        return self.membership_tier == MembershipTier.PREMIUM


# ── Auto-create a UserProfile whenever a new User is saved ───────────────────
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Ensure profile always exists even for legacy users
        UserProfile.objects.get_or_create(user=instance)
