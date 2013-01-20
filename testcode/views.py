# Shawn Jain
# 1/19/2013
# Testcode project
# views.py

# This file defines the logic to display the page. Methods are 
# invoked automatically when a url is matched in urls.py

# imports
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
# Import models 
from testcode.models import *

# This is the landing page
def home(request):
	t = get_template("Student.html")
	stud = Student(name='Shantanu Jain')
	html = t.render(Context({"Student": stud}))
	return HttpResponse(html)