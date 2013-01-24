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
# import for email validation
from django import forms
# import for json 
from django.utils import simplejson

# Import models 
from testcode.models import *

# GLOBAL MINIMUM PASSWORD LENGTH
min_pwd_len = 3

# This is the homepage with login 
def home(request):
	t = get_template("index.html")
	html = t.render(RequestContext(request, {}))
	return HttpResponse(html)

# Student and teacher homepage could be merged, template selected using currentUser.isAdmin

# This is the student navigation page
def student(request):
	# Load user_id with session, match to user, set context based on user
	user_id = request.session["user_id"]
	currentUser = ""
	isNewUser = False
	courses = []
	#print "Session= " + str(user_id)
	# Match to user in DB. If no match, redirect to login
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('')
	#print "USER=" + str(currentUser)
	t = get_template("student-home.html")
	# Find all courses the student is enrolled in via Enrollment query. This is a queryset
	enrollments = Enrollment.objects.filter(user=currentUser.user_id)
	if len(enrollments) == 0:
		isNewUser = True
	for enrollment in enrollments:
		courses.append(Course.objects.get(course_id=enrollment.course)) # May throw an error if not found
	# Use Request Context for pages that load with a CSRF token
	#rc = RequestContext(request, {"user": currentUser, "results": "Nothing Submitted!"}) #doesn't work with template
	rc = Context({"user": currentUser, "isNewUser": isNewUser, "courses": courses, "problems": problems})
	html = t.render(rc)
	return HttpResponse(html)

# This is the teeacher navigation page
def teacher(request):
	# Load user_id with session, match to user, set context based on user
	user_id = request.session["user_id"]
	currentUser = ""
	isNewUser = False
	courses = []
	# Match to user in DB
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('')
	t = get_template("teacher-home.html")
	# Set context based on user - find all associated classes through enrollments 
	enrollments = Enrollment.objects.filter(user=currentUser.user_id)
	if len(enrollments) == 0:
		isNewUser = True
	for enrollment in enrollments:
		courses.append(Course.objects.get(course_id=enrollment.course)) # May throw an error if not found

	# Add stuff for problems. 
	# Use Request Context for pages that load with a CSRF token
	#rc = RequestContext(request, {"user": currentUser, "results": "Nothing Submitted!"})
	rc = Context({"user": currentUser, "isNewUser": isNewUser, "courses": courses})
	html = t.render(rc)
	return HttpResponse(html)


# This is an API function that reads in the submitted data from the 
# form and then renders the output back on the editing page in the 
# solutions textbox.
def submit(request):
	results = "Failure."
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
	isOkay = True
	error = "POST not sent"
	url = ""
	#print request.POST#["email"]
	# Load POST data and read in email and password
	if ("email" in request.POST) and ("password" in request.POST):
		# Attempt to match to entry in database
		if len(User.objects.filter(email=request.POST["email"])) > 0:
			match = User.objects.filter(email=request.POST["email"])[0]
			if match.password == request.POST["password"]: #password and email match
				# Set session user_id var
				request.session["user_id"] = match.user_id
				# check if user.isAdmin, if so, set url to teacher page
				if match.isAdmin:
					url = "/teacher/"
				# else the user is student, set url to student page
				else:
					url = "/student/"
			# otherwise passwords don't match
			else:
				isOkay = False
				error = "Wrong password."
		else:
			isOkay = False
			error = "No email match found."

	# Serialize to JSON and return error 
	errorJsonDict = {}
	errorJsonDict["isOkay"] = isOkay
	errorJsonDict["error"] = error
	errorJsonDict["url"] = url
	errorJson = simplejson.dumps(errorJsonDict)
	return HttpResponse(errorJson, content_type="application/json")

# This is an API function that registers a new user in the database. Checks for uniqueness
# of email address. Only returns JSON with isOkay and error. After successful signup, frontend
# will prompt user for further action
def signup(request):
	isOkay = True
	error = "Sign up successful!"
	#print request.POST
	# Load POST data and read in name, email, password, and isAdmin
	if ("name" in request.POST) and ("email" in request.POST) and ("password" in request.POST) and ("isAdmin" in request.POST):
		# Check for matching email addresses in the database. If the returned array is 0 length,
		# continue registering user. Otherwise, update error
		name = request.POST["name"]
		email = request.POST["email"]
		password = request.POST["password"]
		isAdmin = request.POST["isAdmin"]
		# Check that the fields are not blank.
		if (len(name)>0) and (len(email)>0) and (len(password)>min_pwd_len): #Password must be longer than min_pwd_len chars
			# Try to verify email is valid. If not, catch ValidationError set error
			try:
				f = forms.EmailField()
				f.clean(email)
				if len(User.objects.filter(email=request.POST["email"])) == 0: # no matching email found
					# IMPLEMENT: Validate other fields
					newMember = User(name=name, email=email, password=password, isAdmin=isAdmin)
					newMember.save()
				else:
					isOkay = False
					error = "This email already exists! Please log in."
			except ValidationError:
				isOkay = False
				error = "Invalid Email!"
		else:
			isOkay = False
			error = "Fill in all fields!"
	else:
		isOkay = False
		error = "No POST sent"

	# Serialize errors and send JSON object
	errorJsonDict = {}
	errorJsonDict["error"] = error
	errorJsonDict["isOkay"] = isOkay
	errorJson = simplejson.dumps(errorJsonDict)
	#print errorJson
	return HttpResponse(errorJson, content_type="application/json")

# This is an API function that logs out a current user by deleting their session.
# It forwards the user back to the login page
def logout(request):
	try: 
		del request.session["user_id"]
	except KeyError:
		pass
	return HttpResponseRedirect('')

# This is an API function that takes POST data from the teacher to create a class
# TO IMPLEMENT: The creator is automatically enrolled as the administrator
# Verify the data, save it to the database, and return a JSON
def createcourse(request):
	isOkay = True
	error = ""
	name = ""
	course_id = -1
#	print request.POST
	if ("name" in request.POST) and ("short_name" in request.POST) and ("admin_password" in request.POST) and ("student_password" in request.POST):
#		print request.POST
		name = request.POST["name"]
		short_name = request.POST["short_name"]
		admin_password = request.POST["admin_password"]
		student_password = request.POST["student_password"]
		if (len(name)>0) and (len(short_name)>0) and (len(admin_password)>min_pwd_len) and (len(student_password)>min_pwd_len):
			newCourse = Course(name=name, short_name=short_name, admin_password=admin_password, student_password=student_password)
#			print "saving new course!"
			newCourse.save()
#			print "done saving!"
			course_id = newCourse.course_id
#			print course_id
		else:
			isOkay = False
			error = "Not all fields are filled in."
	else:
		isOkay = False
		error = "YOU IDIOT GIVE ME A POST REQUEST!"
#	print "pre jsondict"
	JsonDict = {}
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	JsonDict["name"] = name
	JsonDict["course_id"] = course_id
	Json = simplejson.dumps(JsonDict)
#	print Json
	return HttpResponse(Json, content_type="application/json")

# This is an API function that reads in the POST request which provides a class
# and returns lectures for that course. -Number of lectures -Number of problems for each lecture
# -Lecture description for each
def getlectures(request):
	isOkay = True
	error = ""
	JsonDict = {}
	if ("course_id" in request.POST):
		course_id = request.POST["course_id"]
		lectures = Lecture.objects.filter(course=course_id)
		for count in range(len(lectures)):
			thisLecture = lectures[count]
			problems = Problem.objects.filter(lecture=thisLecture.lecture_id) # problems associated with thisLecture
			JsonDict["lecture"+str(count)] = thisLecture.description
			JsonDict["problem"+str(count)] = len(problems)
	else:
		isOkay = False
		error = "YOU IDIOT GIVE ME A POST REQUEST!"
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	JsonDict["num_lectures"] = len(lectures)
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# This is an API function that allows a user to add an existing course. Read
# in the POST request's course_id and password and get the user_id from the session. 
# Create an enrollment associating the user and the class. Return a JSON with 
# isOkay, error, course_id, short_name, and num_lectures.
# # lectures, # problems
def addcourse(request):
	isOkay = True
	error = ""
	JsonDict = {}
	if ("course_id" in request.POST) and ("password" in request.POST):
		course_id = request.POST["course_id"]
		student_password = request.POST["password"]
		match = Course.objects.filter(course_id=course_id)
		if len(match) == 0:
			isOkay = False
			error = "No match found!"
		else: # Match found
			if match[0].student_password == student_password:
				user_id = request.session["user_id"] #add user_id validation
				newEnroll = Enrollment(user=user_id, course=course_id) #Initialize submissions?
				newEnroll.save()
				lectures = Lecture.objects.filter(course=course_id)
				JsonDict["course_id"] = course_id
				JsonDict["short_name"] = match[0].short_name
				JsonDict["num_lectures"] = len(lectures)
				# To find number of problems, go through all lectures and find all associated problems
				#JsonDict["num_problems"] = Problem.objects.filter(lecture=)
			else:
				isOkay = False
				error = "Wrong password!"
	else:
		isOkay = False
		error = "YOU IDIOT GIVE ME A POST REQUEST!"
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")
###
# END OF FILE 
###