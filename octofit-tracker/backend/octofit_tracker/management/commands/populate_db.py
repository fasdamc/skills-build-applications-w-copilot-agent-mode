from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

from djongo import models

# Define models for teams, activities, leaderboard, and workouts
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user_email = models.EmailField()
    team = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'email': 'tony@marvel.com', 'username': 'IronMan', 'team': 'Marvel'},
            {'email': 'steve@marvel.com', 'username': 'CaptainAmerica', 'team': 'Marvel'},
            {'email': 'bruce@marvel.com', 'username': 'Hulk', 'team': 'Marvel'},
            {'email': 'clark@dc.com', 'username': 'Superman', 'team': 'DC'},
            {'email': 'bruce@dc.com', 'username': 'Batman', 'team': 'DC'},
            {'email': 'diana@dc.com', 'username': 'WonderWoman', 'team': 'DC'},
        ]
        for u in users:
            User.objects.create_user(email=u['email'], username=u['username'], password='password')

        # Create activities
        Activity.objects.create(user_email='tony@marvel.com', team='Marvel', activity_type='Running', duration=30)
        Activity.objects.create(user_email='steve@marvel.com', team='Marvel', activity_type='Cycling', duration=45)
        Activity.objects.create(user_email='clark@dc.com', team='DC', activity_type='Swimming', duration=60)
        Activity.objects.create(user_email='bruce@dc.com', team='DC', activity_type='Yoga', duration=20)

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=150)
        Leaderboard.objects.create(team='DC', points=120)

        # Create workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='Easy')
        Workout.objects.create(name='HIIT', description='High intensity interval training', difficulty='Hard')

        # Create unique index on email for users collection using pymongo
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)
        client.close()

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
