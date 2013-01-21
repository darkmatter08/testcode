# Shawn Jain
# 1/19/2013
# Testcode project
# views.py

# This file defines the logic to display the page. Methods are 
# invoked automatically when a url is matched in urls.py

# imports
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.template import RequestContext
# Import models 
from testcode.models import *

# This is the homepage with login 
def home(request):
	t = get_template("simplesubmit.html")
	html = t.render(RequestContext())
	return HttpResponse(html)

# This is the student navigation page
def student(request):
	t = get_template("simplesubmit.html")
	stud = Student(name='Shantanu Jain')
	# Use Request Context for pages that load with a CSRF token
	rc = RequestContext(request, {"user": stud, "results": "Nothing Submitted!"})
	html = t.render(rc)
	return HttpResponse(html)

# This is the teeacher navigation page
def teacher(request):
	return HttpResponse("This is the teacher view.")

# This is an API function that reads in the submitted data from the 
# form and then renders the output back on the editing page in the 
# solutions textbox.
def submit(request):
	results = "Failure."
	print "passing through"
	if request.method == 'POST':
		if "solution" in request.POST:
			# Do something with this solution and set the fedback to the "results" var
			solution = request.POST["solution"]
			if solution == "Test input.":
				results = "Good Work There!"
			else:
				results = "Wrong!"
			t = get_template("simplesubmit.html")
			stud = Student(name="Shantanu Jain")
			rc = RequestContext(request, {"user": stud, "results": results})
			html = t.render(rc)
			return HttpResponse(html)

	else:
		return HttpResponseRedirect('')

# This is an API function that verifies the user and sends them to the student page. 
# It forwards to the student or teacher homepage depending on the type of user.
def login(request):
	# Load POST data and read in username and password

	# Match to entry in database
	
	# check if user.isAdmin, if so, load admin page

	# else the user is student, forward to student page