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
# Import for testing function
import commands
import time
# Import models 
from testcode.models import *

# GLOBAL MINIMUM PASSWORD LENGTH
min_pwd_len = 3
# GLOBAL POST REQUEST ERROR STRING
post_request_err = "YOU IDIOT GIVE ME A POST REQUEST!"

# This is the homepage with login 
def landing(request):
	t = get_template("index.html")
	html = t.render(Context({}))#RequestContext(request, {}))
	return HttpResponse(html)

# Student and teacher homepage could be merged, template selected using currentUser.isAdmin

# This is the student navigation page
# Context vars should be courses, lectures, # problems / course, # unsolved problems / course
# problems is "key" in the dict, unsolved problems is the "value" in the dict. Problem is unsolved if there is
# no associated submission.
def student(request):
	# Load user_id with session, match to user, set context based on user
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	isNewUser = False
	courses = []
	# Match to user in DB. If no match, redirect to login
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if currentUser.isAdmin:
		return HttpResponseRedirect('/')
	t = get_template("student-home-new.html")
	# Find all courses the student is enrolled in via Enrollment query. This is a queryset
	enrollments = Enrollment.objects.filter(user=currentUser.user_id)
	if len(enrollments) == 0:
		isNewUser = True
	for enrollment in enrollments:
		courses.append(enrollment.course) # May throw an error if not found
	problems = []
	for thisCourse in courses:
		num_problems = 0
		num_unsolved = 0
		for thisLecture in Lecture.objects.filter(course=thisCourse):
			# used objects.get(), but error raised with many matches
			thisEnrollment = Enrollment.objects.filter(user=currentUser, course=thisCourse)[0] 
			num_problems += len(Problem.objects.filter(lecture=thisLecture))
			num_unsolved = num_problems
			for thisProblem in Problem.objects.filter(lecture=thisLecture):
				if len(Submission.objects.filter(enrollment=thisEnrollment, problem=thisProblem)) > 0: #has a submission 
					num_unsolved -= 1
		problems.append((num_problems, num_unsolved))
	# Use Request Context for pages that load with a CSRF token
	#rc = RequestContext(request, {"user": currentUser, "results": "Nothing Submitted!"}) #doesn't work with template
	rc = Context({"user": currentUser, "isNewUser": isNewUser, "courses": courses, "problems": problems})
	html = t.render(rc)
	return HttpResponse(html)

# This is the teeacher navigation page
def teacher(request):
	# Load user_id with session, match to user, set context based on user
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	isNewUser = False
	courses = []
	# Match to user in DB
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if not currentUser.isAdmin:
		return HttpResponseRedirect('/')
	# Set context based on user - find all associated classes through enrollments 
	enrollments = Enrollment.objects.filter(user=currentUser.user_id)
	if len(enrollments) == 0:
		isNewUser = True
	for enrollment in enrollments:
		courses.append(Course.objects.get(course_id=enrollment.course.course_id)) # May throw an error if not found
	# Create an array of number of lectures, each array element corresponding to the number of lectures in the maching element
	# in the courses queryset. Get length of each queryset via {{some_queryset.count}}
	courseInfo = []
	for course in courses:
	 	assocLectures = Lecture.objects.filter(course=course)
	 	problemCount = 0
	 	for lecture in assocLectures:
	 		problemCount += len(Problem.objects.filter(lecture=lecture))
	 	studentCount = len(Enrollment.objects.filter(course=course)) - 1 # -1 to exclude teacher
	 	courseInfo.append((len(assocLectures), problemCount, studentCount))
	# Add stuff for problems. 
	# Use Request Context for pages that load with a CSRF token
	#rc = RequestContext(request, {"user": currentUser, "results": "Nothing Submitted!"})
	rc = Context({"user": currentUser, "isNewUser": isNewUser, "courses": courses, "courseInfo": courseInfo})
	t = get_template("teacher-home.html")
	html = t.render(rc)
	return HttpResponse(html)

# An API function that allows a student to edit his solution from the editing page. Read in the POST
# request, match the lecture via lecture_id from the URL, find the user, find his enrollment. Create and save a submission. 
# Return JSON with feedback.  
def submitsolution(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
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
		return HttpResponseRedirect('/')

# This is an API function that verifies the user and sends them to the student page. 
# It forwards to the student or teacher homepage depending on the type of user.
def login(request):
	isOkay = True
	error = "POST not sent"
	url = ""
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
	# Load POST data and read in name, email, password, and isAdmin
	if ("name" in request.POST) and ("email" in request.POST) and ("password" in request.POST) and ("isAdmin" in request.POST):
		# Check for matching email addresses in the database. If the returned array is 0 length,
		# continue registering user. Otherwise, update error
		name = request.POST["name"]
		email = request.POST["email"]
		password = request.POST["password"]
		isAdmin = request.POST["isAdmin"]
		# Check that the fields are not blank.
		if int(isAdmin) == 0:
			isAdmin = False
		else:
			isAdmin = True
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
	return HttpResponse(errorJson, content_type="application/json")

# This is an API function that logs out a current user by deleting their session.
# It forwards the user back to the login page
def logout(request):
	try: 
		del request.session["user_id"]
	except KeyError:
		pass
	return HttpResponseRedirect('/')

# This is an API function that takes POST data from the teacher to create a class
# The creator is automatically enrolled as the administrator
# Verify the data, save it to the database, and return a JSON
def createcourse(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	isOkay = True
	error = ""
	name = ""
	course_id = -1
	if ("name" in request.POST) and ("short_name" in request.POST) and ("student_password" in request.POST):
		name = request.POST["name"]
		short_name = request.POST["short_name"]
		student_password = request.POST["student_password"]
		# name = "weird class"
		# short_name = "Weird"
		# student_password = "asdf"
		if (len(name)>0) and (len(short_name)>0) and (len(student_password)>min_pwd_len):
			newCourse = Course(name=name, short_name=short_name, student_password=student_password)
			newCourse.save()
			course_id = newCourse.course_id
			error = "Class created successfully!"
			# Add Enrollment with current user.
			enroll = Enrollment(user=User.objects.get(user_id=user_id), course=Course.objects.get(course_id=course_id))
			enroll.save()
		else:
			isOkay = False
			error = "Not all fields are filled in."
	else:
		isOkay = False
		error = post_request_err
	JsonDict = {}
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	JsonDict["name"] = name
	JsonDict["course_id"] = course_id
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# This is an API function that reads in the POST request which provides a course_id
# and returns lectures for that course. -Number of lectures -Number of problems for each lecture
# -Lecture description for each
def getlectures(request):
	isOkay = True
	error = ""
	JsonDict = {}
	if ("course_id" in request.POST):
		course_id = request.POST["course_id"]
		course = Course.objects.get(course_id=course_id)
		lectures = Lecture.objects.filter(course=course)
		lecture_name = []
		lecture_id = []
		for count in range(len(lectures)):
			thisLecture = lectures[count]
			problems = Problem.objects.filter(lecture=thisLecture.lecture_id) # problems associated with thisLecture
			lecture_name.append(thisLecture.description)
			lecture_id.append(thisLecture.lecture_id)
			#JsonDict["problem"][str(count)] = len(problems)  
		JsonDict["lecture_name"] = lecture_name
		JsonDict["lecture_id"] = lecture_id
		JsonDict["password"] = course.student_password
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	JsonDict["num_lectures"] = len(lectures)
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# This is an API function that allows a user to add an existing course. Read
# in the POST request's course_id and password and get the user_id from the session. 
# Create an enrollment associating the user and the class, disallowing double enrollments
# Return a JSON with isOkay, error, course_id, short_name, and num_lectures.
# # lectures, # problems
def addcourse(request):
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	isOkay = True
	error = ""
	JsonDict = {}
	problems = 0
	if ("course_id" in request.POST) and ("password" in request.POST):
		course_id_temp = request.POST["course_id"]
		course_id = -1
		try:
			course_id = int(course_id_temp)
			student_password = request.POST["password"]
			matches = Course.objects.filter(course_id=course_id)
			if len(matches) == 0:
				isOkay = False
				error = "No match found!"
			else: # Match found
				match = matches[0]
				if match.student_password == student_password:
					#check for exisitng matching enrollment
					checkEnroll = Enrollment.objects.filter(user=currentUser, course=match)
					if len(checkEnroll) == 0: 
						newEnroll = Enrollment(user=currentUser, course=match) #Initialize submissions?
						newEnroll.save()
						lectures = Lecture.objects.filter(course=match)
						for lecture in lectures:
							problems += len(Problem.objects.filter(lecture=lecture))
						JsonDict["course_id"] = match.course_id
						JsonDict["name"] = match.name
						JsonDict["num_lectures"] = len(lectures)
						# To find number of problems, go through all lectures and find all associated problems
						JsonDict["num_problems"] = problems
					else:
						isOkay = False
						error = "You are already enrolled in the class!"
				else:
					isOkay = False
					error = "Wrong password!"
		except ValueError: # rasied from casting int 
			isOkay = False
			error = "Course ID was not valid! Integers only."
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# This is an API function that allows a teacher to add a Lecture to a class. Read in the POST
# request with course_id. 
def createlecture(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	isOkay = True
	error = ""
	name = ""
	lecture_id = -1
	JsonDict = {}
	if ("course_id" in request.POST) and ("name" in request.POST):
		name = request.POST["name"]
		course_id = request.POST["course_id"]
		if len(name) > 0:
			newLecture = Lecture(description=name, course=Course.objects.get(course_id=course_id))
			newLecture.save()
			lecture_id = newLecture.lecture_id
		else:
			isOkay = False
			error = "No name entered!"
	else:
		isOkay = False
		error = post_request_err
	JsonDict["lecture_id"] = lecture_id
	JsonDict["name"] = name
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# This function renders the editing page for students. Get the lecture_id from the URL, get user_id from session, 
# match to an enrollment, get the most recent submission for the first problem in the lecture, pass all problems in the template. 
# TO IMPLEMENT: Check user.isAdmin = False
def edit(request, mylecture_id):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if currentUser.isAdmin:
		return HttpResponseRedirect('/')
	lectures = Lecture.objects.filter(lecture_id=mylecture_id)
	if len(lectures) == 0:
		return HttpResponseRedirect('/student')
	lecture = lectures[0]
	course = lecture.course
	enrollment = Enrollment.objects.get(user=currentUser, course=course)
	problems = Problem.objects.filter(lecture=lecture)
	activeProblem = problems[0] #will choose first problem 
	context = Context({"activeProblem": activeProblem, "problems": problems, "lecture": lecture, "course": course, "user": currentUser})
	t = get_template("Student.html")
	html = t.render(context)#RequestContext(request, {}))
	return HttpResponse(html)

# An API function that allows a teacher to submit a problem for the students to edit. 
# JSON always returns isOkay and error string.
# If the client only sends a problem_name and lecture_id (blank description) in the POST, then create a problem and 
# return JSON with problem_id. If client POSTs problem_id, description, initial_code, and timeout (ms) in the POST, then update the problem. 
def createproblem(request):
	print request.POST
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	isOkay = True
	error = ""
	JsonDict = {}
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	# Case 1 - only problem_name and lecture_id, return problem_id
	if ("lecture_id" in request.POST) and ("problem_name" in request.POST):
		lecture_id = request.POST["lecture_id"]
		problem_name = request.POST["problem_name"]
		# lecture_id = 2
		# problem_name = "fix this bug!"
		if len(problem_name) > 0:
			lecture = Lecture.objects.get(lecture_id=lecture_id)
			newProblemNumber = 0
			allProblems = Problem.objects.filter(lecture=lecture).order_by('-problem_number')
			if len(allProblems) == 0:
				newProblemNumber = 1
			else:
				newProblemNumber = allProblems[0].problem_number + 1
			newProblem = Problem(name=problem_name, lecture=lecture, problem_number=newProblemNumber, description="", initial_code="")
			newProblem.save()
			# Create blank testcase, testcause_number = 1
			firstTestcase = Testcase(testcase_number=1, problem=newProblem, input_value="", expected_output="")
			firstTestcase.save()
			problem_id = newProblem.problem_id
			JsonDict["problem_id"] = problem_id
			#JsonDict["problem_name"] = problem_name
		else:
			isOkay = False
			error = "Fill in all fields!"
	# Case 2 - problem_id, description, initial_code, timeout
	elif ("problem_id" in request.POST) and ("description" in request.POST) and ("initial_code" in request.POST):
		print request.POST
		problem_id = request.POST["problem_id"]
		description = request.POST["description"]
		initial_code = request.POST["initial_code"]
		if len(description) > 0:
			print "getting problem"
			problem = Problem.objects.get(problem_id=problem_id)
			print "got problem"
			problem.description = description
			problem.initial_code = initial_code
			problem.save()
		else:
			isOkay = False
			error = "Nothing in the description!"
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# An API function that returns the previous or next submission from the submission history. 
# Reads in nextSubmission and submission_id from the POST request and returns a JSON with
# isOkay, error, and solution.
def submissionHistory(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	isOkay = True
	error = ""
	hasNext = True
	hasPrev = True
	JsonDict = {}
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if ("isNextSubmission" in request.POST) and ("submission_id" in request.POST):
		isNextSubmission = request.POST["isNextSubmission"]
		submission_id = request.POST["submission_id"]
		currentSubmission = Submission.objects.get(submission_id=submission_id)
		allSubmissions = Submission.objects.filter(problem=currentSubmission.problem)
		if int(isNextSubmission) == 1: #nextSubmission == True
			allSubmissions = Submission.objects.filter(problem=currentSubmission.problem).order_by('-date')
			nextSubmissionIndex = -1
			for i in range(len(allSubmissions)):
				if allSubmissions[i].submission_id == currentSubmission.submission_id:
					nextSubmissionIndex = i - 1
			if nextSubmissionIndex < 0:
				isOkay = False
				error = "No more submissions!"
			else:
				nextSubmission = allSubmissions[nextSubmissionIndex]
				JsonDict["solution"] = nextSubmission.solution
				JsonDict["submission_id"] = nextSubmission.submission_id
			if nextSubmissionIndex == 0:
				hasNext = False
		else:
			allSubmissions = Submission.objects.filter(problem=currentSubmission.problem).order_by('date')
			prevSubmissionIndex = -1
			for i in range(len(allSubmissions)):
				if allSubmissions[i].submission_id == currentSubmission.submission_id:
					prevSubmissionIndex = i - 1
			if prevSubmissionIndex < 0:
				isOkay = False
				error = "No more submissions!"
			else:
				prevSubmission = allSubmissions[prevSubmissionIndex]
				JsonDict["solution"] = prevSubmission.solution
				JsonDict["submission_id"] = prevSubmission.submission_id
			if prevSubmissionIndex == 0:
				hasPrev = False
	else:
		isOkay = False
		error = post_request_err
	JsonDict["hasNext"] = hasNext
	JsonDict["hasPrev"] = hasPrev
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# API function that allows a teacher to submit a test case for a particular problem. 
# Takes problem_id, input_value, expected_output, and testcase_number from the POST request, returns a JSON 
# with isOkay, error
def createtestcase(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	isOkay = True
	error = ""
	JsonDict = {}
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if ("problem_id" in request.POST) and ("input_value" in request.POST) and ("expected_output" in request.POST) and ("testcase_number" in request.POST):
		problem_id = request.POST["problem_id"]
		input_value = request.POST["input_value"]
		expected_output = request.POST["expected_output"]
		testcase_number = request.POST["testcase_number"]
		problem = Problem.objects.get(problem_id=problem_id)
		if len(input_value) > 0 and len(expected_output) > 0 and testcase_number > 0:
			# Split into new vs. exisiting testcase based on testcase_number
			testcaseQuerySet = Testcase.objects.filter(testcase_number=testcase_number, problem=problem)
			if len(testcaseQuerySet) == 0:
				newTestcase = Testcase(problem=problem, expected_output=expected_output, input_value=input_value, testcase_number=testcase_number)
				newTestcase.save()
				JsonDict["testcase_id"] = newTestcase.testcase_id
			else:
				matchingTestcase = testcaseQuerySet[0]
				matchingTestcase.expected_output = expected_output
				matchingTestcase.input_value = input_value
				matchingTestcase.save()
		else:
			isOkay = False
			error = "Not all fields filled!"
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# An API function that allows the student to switch between problems on the editing page. 
# From POST, reads in problem_id, from the session, user_id. It returns a JSON with the 
# problem_id, problem_description, name, lecture_id, and solution - from the latest submission
# Also returns an array of testcases - each element is an array with [0] being inputs and [1] being expected_output
def getproblem(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	isOkay = True
	error = ""
	JsonDict = {}
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if ("problem_id" in request.POST):
		problem_id = request.POST["problem_id"]
		problem = Problem.objects.get(problem_id=problem_id)
		testcases = []
		allTestcases = Testcase.objects.filter(problem=problem)
		currentEnrollment =  Enrollment.objects.get(user=currentUser, course=problem.lecture.course)
		for testcase in allTestcases:
			testcases.append((testcase.input_value, testcase.expected_output))
		allSubmissions = Submission.objects.filter(problem=problem, enrollment=currentEnrollment).order_by('-date')
		# Check if there are any matching submissions. If not, create a submission.
		if len(allSubmissions) == 0: #No submission yet. Send blank solution and don't send submission_id
			JsonDict["solution"] = problem.initial_code
		else:
			latestSubmission = allSubmissions[0]
			JsonDict["solution"] = latestSubmission.solution
			JsonDict["submission_id"] = latestSubmission.submission_id
		JsonDict["testcases"] = testcases
		JsonDict["problem_id"] = problem_id
		JsonDict["description"] = problem.description
		JsonDict["name"] = problem.name
		#JsonDict["lecture_id"] = problem.lecture.lecture_id
		#HasPrev code#####
		allSubmissionsReordered = allSubmissions.order_by('date')
		prevSubmissionIndex = -1
		hasPrev = True
		for i in range(len(allSubmissionsReordered)):
			if allSubmissionsReordered[i].submission_id == latestSubmission.submission_id:
				prevSubmissionIndex = i-1
		if prevSubmissionIndex < 0:
			hasPrev = False
		JsonDict["hasPrev"] = hasPrev
		#####
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# Renders the teacher-lecture page with the context vars. Includes # of users who have a submission for a particular problem
def teacherlecture(request, lecture_id):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	lectures = Lecture.objects.filter(lecture_id=lecture_id)
	if len(lectures) == 0:
		return HttpResponseRedirect('/teacher')
	lecture = lectures[0]
	course = lecture.course
	#problems = Problem.objects.filter(lecture=lecture_id)
	allProblems = Problem.objects.filter(lecture=lecture_id)
	problems = []
	for problem in allProblems:
		# Get all enrollments. Check if they have any submissions, if so, increment numSubmissions by 1 for this problem.
		enrollments = Enrollment.objects.filter(problem=problem)
		numSubmissions = 0
		for enrollment in enrollments:
			# Get submissions for this problem. If more than 1, increment counter.
			if len(Submission.objects.filter(enrollment=enrollment)) > 0:
				numSubmissions += 1
		problems.append((problem, numSubmissions))
	t = get_template("teacher-lecture.html")
	rc = Context({"user": currentUser, "course": course, "lecture": lecture, "problems": problems})
	html = t.render(rc)#RequestContext(request, {}))
	return HttpResponse(html)

# API function that gets problem_id in POST, returns JSON with problem_description, problem_name
def getproblemteacher(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	isOkay = True
	error = ""
	JsonDict = {}
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if ("problem_id" in request.POST):
		problem_id = request.POST["problem_id"]
		problem = Problem.objects.get(problem_id=problem_id)
		allSubmissions = Submission.objects.filter(problem=problem).order_by('-date')
		problem_description = problem.description
		# list of all testcase inputs and outputs. 
		allTestcases = Testcase.objects.filter(problem=problem).order_by('testcase_number')
		testcase_input = []
		testcase_output = []
		for testcase in allTestcases:
			testcase_input.append(testcase.input_value)
			testcase_output.append(testcase.expected_output)
		JsonDict["problem_description"] = problem_description
		JsonDict["name"] = problem.name
		JsonDict["testcase_input"] = testcase_input
		JsonDict["testcase_output"] = testcase_output
		JsonDict["initial_code"] = problem.initial_code
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# Recieves problem_id, solution, creates submission, runs the student's code.
# Returns submission_id, feedback. If submission is identical to the previous
def saveandrun(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	isOkay = True
	error = ""
	JsonDict = {}
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if ("problem_id" in request.POST) and ("solution" in request.POST):	
		problem_id = request.POST["problem_id"]
		solution = request.POST["solution"]
		problem = Problem.objects.get(problem_id=problem_id)
		if len(solution) > 0:
			enrollment = Enrollment.objects.get(course=problem.lecture.course, user=currentUser)
			newSubmission = Submission(solution=solution, enrollment=enrollment, problem=problem, grade="[]")
			submissions = Submission.objects.filter(problem=problem, enrollment=enrollment).order_by('-date')
			if len(submissions) > 0:
				if submissions[0].solution == solution:
					newSubmission = submissions[0]
			#newSubmission.save()
			testcases = Testcase.objects.filter(problem=problem).order_by('testcase_number')
			results = []
			inputs = []
			expected_outputs = []
			outputs = []
			errors = []
			for testcase in testcases:
				result = test(testcase, newSubmission)
				results.append(result[1])
				outputs.append(result[0])
				inputs.append(testcase.input_value)
				expected_outputs.append(testcase.expected_output)
				errors.append(result[2])
				print results
			newSubmission.grade=str(results) #returns JSON with results of all testcases
			print "Saving..."
			newSubmission.save()
			print "making json dicts"
			JsonDict["grade"] = results
			JsonDict["inputs"] = inputs
			JsonDict["expected_outputs"] = expected_outputs
			JsonDict["outputs"] = outputs
			JsonDict["errors"] = errors
		else:
			isOkay = False
			error = "Please fill in all fields!"
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	print Json
	return HttpResponse(Json, content_type="application/json")

# An API function that redirects the user based on user.isAdmin. Implemented for the "home" button
def home(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if currentUser.isAdmin:
		return HttpResponseRedirect('/teacher')
	else:
		return HttpResponseRedirect('/student')

# API function that returns all testcase results by student for the latest submission. 
# Requires problem_id
def viewperformance(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	JsonDict = {}
	if ("problem_id" in request.POST):
		problem_id = request.POST["problem_id"]
		problem = Problem.objects.get(problem_id=problem_id)
		course = problem.lecture.course
		# find all enrollments
		enrollments = Enrollment.objects.filter(course=course)
		# find submissions by enrollment. Take most recent append it. 
		submissionidarray = []
		name = []
		date = []
		grade = []
		unsubmitted = []
		for enrollment in enrollments:
			submissions = Submission.objects.filter(enrollment=enrollment, problem=problem).order_by('-date')
			if len(submissions) > 0:
				submission = submissions[0]
				#submissionInfo = (submission.submission_id, enrollment.user.name, unicode(submission.date)[:-19], submission.grade)
				submissionidarray.append(submission.submission_id)
				name.append(enrollment.user.name)
				date.append(unicode(submission.date)[:-22])
				grade.append(submission.grade)
				#print submissionInfo
				#results.append(submissionInfo)
				#print "results appended!"
				#print results
			else: # no submission for this problem. 
				if not enrollment.user.isAdmin:
					unsubmitted.append(enrollment.user.name)
		JsonDict["submission_id"] = submissionidarray
		JsonDict["name"] = name
		JsonDict["date"] = date
		JsonDict["grade"] = grade
		JsonDict["unsubmitted"] = unsubmitted
	else:
		isOkay = False
		error = post_request_err
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# Internal function that runs a submssion against a test case. Returns True if the test was passed or False if the test failed
def test(testcase, submission):
	input_value = testcase.input_value
	expected_output = testcase.expected_output
	solution = submission.solution
	inputFile = solution

	from ideone.ideone import *
	ideone = IdeOne()
	python = 4
	link = ideone.createSubmission(inputFile, python, input=input_value)

	# wait for it to finish 
	while ideone.getSubmissionStatus(link)[0] != Status.Done:
	    print "sending to external server..."
	    pass

	output =  ideone.getSubmissionDetails(link)['output']
	error = ideone.getSubmissionDetails(link)['stderr']
	return (output, (output == (expected_output + "\n")), error)

# Return # students with submissions, testcases

def studentperformance(request, problem_id):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	problem = Problem.objects.get(problem_id=problem_id)
	lecture = problem.lecture
	course = lecture.course
	testcases = Testcase.objects.filter(problem=problem)
	enrollments = Enrollment.objects.filter(course=course)
	submissions = 0
	for enrollment in enrollments:
		if len(Submission.objects.filter(problem=problem)) > 0:
			submissions += 1
	t = get_template("teacher-analyze.html")
	rc = Context({"user": currentUser, "course": course, "lecture": lecture, "problem": problem, "testcases": testcases, "submissions": submissions})
	html = t.render(rc)#RequestContext(request, {}))
	return HttpResponse(html)

def getSubmission(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	JsonDict = {}
	if ("submission_id" in request.POST):
		submission_id = request.POST["submission_id"]
		submssion = ""
		submissions = Submission.objects.filter(submission_id=submission_id)
		if len(submissions) > 0:
			submission = submissions[0]
			JsonDict["solution"] = submission.solution
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

# API function that checks for password, returns True if matching. 
# Recieves name, password, email, and updates them
def account(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	JsonDict = {}
	if ("name" in request.POST) and ("new_password" in request.POST) and ("old_password" in request.POST)and ("email" in request.POST):
		name = request.POST["name"]
		new_password = request.POST["new_password"]
		old_password = request.POST["old_password"]
		email = request.POST["email"]
		if old_password == currentUser.password:
			currentUser.name = name
			currentUser.password = new_password
			currentUser.email = email
			currentUser.save()
			error = "Save successful."
			JsonDict["isOkay"] = True
			JsonDict["error"] = error
		else:
			JsonDict["isOkay"] = False
			JsonDict["error"] = "Wrong login information."
	elif: #return values case
		JsonDict["name"] = currentUser.name
		JsonDict["email"] = currentUser.email
		JsonDict["isOkay"] = True
		JsonDict["error"] = ""
	else:
		isOkay = False
		error = post_request_err
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

def getlogin(request):
	user_id = 0
	try:
		user_id = request.session["user_id"]
	except KeyError:
		return HttpResponseRedirect('/')
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	JsonDict = {}
	isOkay = True
	error  = ""
	if ("course_id" in request.POST):
		password = ""
		course_id = request.POST["course_id"]
		courses = Course.objects.filter(course_id=course_id)
		if len(courses) > 0:
			password = courses[0].student_password
			JsonDict["password"] = password
		else:
			isOkay = False
			error = "Invalid course id"
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")
# def fixthis(request):
# 	#testcase = Testcase(input_value="x = addTwo(1,2)\n", expected_output="x == 3", testcase_number=99,)
# 	#output = test(testcase, newSubmission)

# 	input_value = "x = addTwo(1,2)\n"
# 	expected_output = "x == 3"
# 	solution = "def addTwo(a, b):\n\treturn a+b"
# 	timeout = 5
# 	# Create the test file by adding (1)submission.solution (2)input_value (3)if (4)expected_output (5): (6) return True (6) return False 
# 	inputFile = solution + "\n" + input_value + "\n" + "if " + expected_output + ":" + "\n" + "\t" + "print True" + "\n" + "else:" + "\n" + "\t" + "print False"

# 	from ideone.ideone import *
# 	ideone = IdeOne()
# 	# run a python program
# 	python = 4

# 	link = ideone.createSubmission(inputFile, python, input=input_value)

# 	# wait for it to finish 
# 	while ideone.getSubmissionStatus(link)[0] != Status.Done:
# 	    pass

# 	output =  ideone.getSubmissionDetails(link)['output']

# 	return HttpResponse("<p>" + inputFile + "</p>" + output)

###
# END OF FILE 
###