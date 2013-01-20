# Shawn Jain
# 1/19/2013
# Testcode project
# models.py

# Data Models within the store app

#imports
from django.db import models
from django.forms import ModelForm

# Create your models here.
class Student(models.Model):
	name = models.CharField(max_length=30)

	#Describes the object when it is called from the DB
	def __unicode__(self):
		return 

class Course(models.Model):

class Lecture(models.Model):

class Problem(models.Model):