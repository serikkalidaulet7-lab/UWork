from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BookingReservation(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40)
    guest_count = models.PositiveSmallIntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name


class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track_name = models.CharField(max_length=120, default='Architecture pathway')
    sessions_completed = models.PositiveIntegerField(default=0)
    tasks_unlocked = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=1)
    tree_tokens = models.PositiveIntegerField(default=0)
    trees_planted = models.PositiveIntegerField(default=0)
    hero_level = models.PositiveIntegerField(default=1)
    impact_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} progress'

    def complete_session(self):
        self.sessions_completed += 1
        self.streak += 1
        self.impact_points += 12

        if self.sessions_completed % 3 == 0:
            self.tasks_unlocked += 1
        if self.sessions_completed % 5 == 0:
            self.tree_tokens += 1
        if self.sessions_completed % 10 == 0:
            self.hero_level += 1

    def plant_tree(self):
        if self.tree_tokens > 0:
            self.tree_tokens -= 1
            self.trees_planted += 1
            self.impact_points += 25
            return True
        return False


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_progress(sender, instance, created, **kwargs):
    if created:
        UserProgress.objects.create(user=instance)
