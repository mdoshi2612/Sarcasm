from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from game.models import Level,BonusQuestion
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
# class userdata(models.Model):
# 	username=models.CharField(max_length=200)
# 	email=models.CharField(max_length=200)
# 	roll=models.CharField(max_length=9)
# 	referral=models.CharField(max_length=100,default=0)
# 	referral_count=models.IntegerField(default=0)
DEPARTMENTS = [u'Aerospace Engineering',  
        u'Centre for Environmental Science and Engineering',
        u'Chemical Engineering', 
        u'Chemistry',
        u'Civil Engineering', 
        u'Computer Science & Engineering',
        u'Electrical Engineering', 
        u'Energy Science and Engineering', 
        u'Humanities & Social Science',
        u'Mathematics', 
        u'Mechanical Engineering',
        u'Metallurgical Engineering & Materials Science', 
        u'Physics', 
        u'Others'
        ]

class Team(models.Model):
	leader_name = models.CharField(max_length=100)
	leader_roll_number = models.CharField(max_length=100)
	year_of_study = models.CharField(max_length=100)
	team_name = models.CharField(max_length=100)
	team_logo = models.CharField(max_length=100)
	player1 = models.CharField(max_length=100)
	player2 = models.CharField(max_length=100)
	player3 = models.CharField(max_length=100)
	player4 = models.CharField(max_length=100)


class Player(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	username=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	roll=models.CharField(default='0', max_length=9)
	referral=models.CharField(max_length=100,default=0)
	referral_count = models.IntegerField(default=0)
	bonus_attempted = models.IntegerField(default=0)
	address = models.CharField(max_length=500, null=False, blank=False)
	current_level = models.ForeignKey(Level, default=Level.DEFAULT_LEVEL, on_delete=models.CASCADE)
	current_level_time = models.DateTimeField(default=timezone.now)
	bonus_level_id = models.IntegerField(default=1)
	department = models.CharField(max_length=255, null=False, blank=False,
                                  choices=tuple([(dept, dept) for dept in DEPARTMENTS]))
	points=models.IntegerField(default=0)
	details_done = models.BooleanField(default=0)
	
	
	def __str__(self):
		return self.user.username
	
	def get_level(self):
		return self.current_level.level_id

	def get_name(self):
		return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Player.objects.create(user=instance)
	instance.player.save()

