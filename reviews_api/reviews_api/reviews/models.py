# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User


from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db import models

# Create your models here.
import numpy as np

# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length = 300)
	def average(self):
		all_ratings = map(lambda x: x.rating, self.review_set.all())
		return np.mean(all_ratings)

	def __unicode__(self):
		return self.name
class Reviews(models.Model):	
	'''
	Rating - must be between 1 - 5
	Title - no more than 64 chars
	Summary - no more than 10k chars
	IP Address - IP of the review submitter
	Submission date - the date the review was submitted
	Company - information about the company for which the review was submitted, can be simple text (e.g., name, company id, etc.) or a separate model altogether
	Reviewer Metadata - information about the reviewer, can be simple text (e.g., name, email, reviewer id, etc.) or a separate model altogether

	'''
	RATINGS_CHOICES = (
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5'),
	)
	
	company     = models.ForeignKey(Company)
	pub_date    = models.DateTimeField(null=True, blank=True)
	user_name   = models.CharField(max_length = 200) 
	comment     = models.CharField(max_length = 200)
	rating 	    = models.IntegerField(choices = RATINGS_CHOICES)
	title 	    = models.CharField(max_length = 64)
	summary     = models.CharField(max_length = 10000)
	#ip_address  = models.GenericIPAddressField(protocol='IPv4', verbose_name="Last Login IP", default="127.0.0.1")
	ip_address = models.CharField(null=True,max_length = 120, default="ABC")
	owner       = models.ForeignKey('auth.User', related_name='reviews', on_delete=models.CASCADE)
	

	def __str__(self):
		"""Return a human readable representation of the model instance."""
		return "{}".format(self.name)


# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)