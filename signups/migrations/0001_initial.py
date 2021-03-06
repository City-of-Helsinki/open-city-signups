# Generated by Django 2.0.5 on 2018-05-15 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('cancelled_at', models.DateTimeField(blank=True, null=True, verbose_name='cancelled at')),
            ],
            options={
                'verbose_name': 'sign-up',
                'verbose_name_plural': 'sign-ups',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='SignupTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(unique=True, max_length=100, verbose_name='identifier')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('users', models.ManyToManyField(related_name='signup_targets', through='signups.Signup', to=settings.AUTH_USER_MODEL, verbose_name='users')),
            ],
            options={
                'verbose_name': 'sign-up target',
                'verbose_name_plural': 'sign-up targets',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='signup',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signups', to='signups.SignupTarget', verbose_name='target'),
        ),
        migrations.AddField(
            model_name='signup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signups', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
