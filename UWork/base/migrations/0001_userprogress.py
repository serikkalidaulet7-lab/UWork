from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_progress_for_existing_users(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    UserProgress = apps.get_model('base', 'UserProgress')
    for user in User.objects.all():
        UserProgress.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_name', models.CharField(default='Architecture pathway', max_length=120)),
                ('sessions_completed', models.PositiveIntegerField(default=0)),
                ('tasks_unlocked', models.PositiveIntegerField(default=0)),
                ('streak', models.PositiveIntegerField(default=1)),
                ('tree_tokens', models.PositiveIntegerField(default=0)),
                ('trees_planted', models.PositiveIntegerField(default=0)),
                ('hero_level', models.PositiveIntegerField(default=1)),
                ('impact_points', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_progress_for_existing_users, migrations.RunPython.noop),
    ]
