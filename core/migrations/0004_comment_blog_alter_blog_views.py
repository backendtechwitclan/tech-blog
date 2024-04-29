# Generated by Django 4.2 on 2024-04-28 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_blog_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.blog'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blog',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='views', to=settings.AUTH_USER_MODEL),
        ),
    ]