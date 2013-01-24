# Shawn Jain
# 1/19/2013
# Testcode project
# models.py

# Data Models within the store app

# imports
from django.db import models
from django.forms import ModelForm

# Create your models here.

# Each course is unique to each semester and each section. 
# For example, 6.006 Fall Morning has a different course_id than 
# 6.006 Fall Afternoon, and also different than 6.006 Spring Morning
class Course(models.Model):
	# custom primary key, via auto incrementing field
	course_id = models.AutoField(primary_key=True)
	# corresponds to MIT course number
	short_name = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	admin_password = models.CharField(max_length=30) 
	student_password = models.CharField(max_length=30)
	
	# Describes the object when it is called from the DB
	def __unicode__(self):
		return str(self.short_name)

class User(models.Model):
	# custom primary key, via auto incrementing field
	user_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	email = models.EmailField(unique=True) #should be unique on the column
	isAdmin = models.BooleanField()

	# Many to many relationship with course via enrollment
	course = models.ManyToManyField(Course, through='Enrollment')

	# Describes the object when it is called from the DB
	def __unicode__(self):
		return "name="+self.name+" user_id="+str(self.user_id)

class Lecture(models.Model):
	# custom primary key, via auto incrementing field
	lecture_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	# Many to one relationships with Course - one Course has many Lectures
	course = models.ForeignKey(Course)

	# Describes the object when it is called from the DB
	def __unicode__(self):
		return self.description

class Problem(models.Model):
	# custom primary key, via auto incrementing field
	problem_id = models.AutoField(primary_key=True)
	description = models.TextField(max_length=100)
	# Many to one relationships with Lecture - one Lecture has many Problems
	lecture = models.ForeignKey(Lecture)
	# Many to many relationships with Enrollment via Submission
	#enrollment = models.ManyToManyField(Enrollment, through='Submission')

	# Describes the object when it is called from the DB
	def __unicode__(self):
		return "problem_id="+str(self.problem_id)+" description="+self.description

# TRANSACTION TABLES

class Enrollment(models.Model):
	# custom primary key, via auto incrementing field
	enrollment_id = models.AutoField(primary_key=True)
	enrollmentDate = models.DateTimeField(auto_now_add=True, auto_now=True)
	user = models.ForeignKey(User)
	course = models.ForeignKey(Course)
	# Many to Many Relationship with problems via submission
	problem = models.ManyToManyField(Problem, through='Submission')

	# Describes the object when it is called from the DB
	def __unicode__(self):
		return "user="+str(self.user)+" course="+str(self.course)

class Submission(models.Model):
	# custom primary key, via auto incrementing field
	submission_id = models.AutoField(primary_key=True)
	solution = models.TextField(max_length=100)
	enrollment = models.ForeignKey(Enrollment)
	problem = models.ForeignKey(Problem)
	grade = models.DecimalField(max_digits=3, decimal_places=2)
	date = models.DateTimeField(auto_now_add=True, auto_now=True)

	# Describes the object when it is called from the DB
	def __unicode__(self):
		return "solution="+self.solution+" problem="+str(self.problem)