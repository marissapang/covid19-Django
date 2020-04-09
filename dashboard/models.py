from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

default_country_selections = '["Global", "United States", "China", "Italy"]'
default_state_selections = '[]'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dashboard_countries = models.CharField(max_length=9999, blank=True)
    dashboard_states = models.CharField(max_length=9999, blank=True)

    def __str__(self):
    	return str(self.user)+"--"+self.dashboard_countries+"--"+self.dashboard_states

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance, dashboard_countries = default_country_selections, dashboard_states = default_state_selections)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

