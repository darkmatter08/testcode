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
# GLOBAL POST REQUEST ERROR STRING
post_request_err = "YOU IDIOT GIVE ME A POST REQUEST!"

# This is the homepage with login 
def home(request):
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
	user_id = request.session["user_id"]
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
	t = get_template("student-home.html")
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
	user_id = request.session["user_id"]
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
	lectures = []
	for course in courses:
	 	lectures.append(Lecture.objects.filter(course=course)[0])
	# Add stuff for problems. 
	# Use Request Context for pages that load with a CSRF token
	#rc = RequestContext(request, {"user": currentUser, "results": "Nothing Submitted!"})
	rc = Context({"user": currentUser, "isNewUser": isNewUser, "courses": courses})
	t = get_template("teacher-home.html")
	html = t.render(rc)
	return HttpResponse(html)

# An API function that allows a student to edit his solution from the editing page. Read in the POST
# request, match the lecture via lecture_id from the URL, find the user, find his enrollment. Create and save a submission. 
# Return JSON with feedback.  
def submitsolution(request):
	user_id = request.session["user_id"]
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
	user_id = request.session["user_id"]
	isOkay = True
	error = ""
	name = ""
	course_id = -1
	if ("name" in request.POST) and ("short_name" in request.POST) and ("admin_password" in request.POST) and ("student_password" in request.POST):
		name = request.POST["name"]
		short_name = request.POST["short_name"]
		admin_password = request.POST["admin_password"]
		student_password = request.POST["student_password"]
		if (len(name)>0) and (len(short_name)>0) and (len(admin_password)>min_pwd_len) and (len(student_password)>min_pwd_len):
			newCourse = Course(name=name, short_name=short_name, admin_password=admin_password, student_password=student_password)
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
		lectures = Lecture.objects.filter(course=Course.objects.get(course_id=course_id))
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
			match = ""
			if len(matches) == 0:
				isOkay = False
				error = "No match found!"
			else: # Match found
				match = matches[0]
				if match.student_password == student_password:
					user_id = request.session["user_id"] #add user_id validation
					currentUser = "" # REMOVE
					try:
						currentUser = User.objects.get(user_id=user_id)
					except User.DoesNotExist:
						return HttpResponseRedirect('/')
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
	isOkay = True
	error = ""
	name = ""
	lecture_id = -1
	JsonDict = {}
	user_id = request.session["user_id"]
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
	user_id = request.session["user_id"]
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if currentUser.isAdmin:
		return HttpResponseRedirect('/')
	lecture = Lecture.objects.get(lecture_id=mylecture_id)
	course = lecture.course
	enrollment = Enrollment.objects.get(user=currentUser, course=course)
	problems = Problem.objects.filter(lecture=lecture)
	activeProblem = problems[0] #will choose first problem 
	# Get most recent submission. Check if it has a submission, if not, create a blank submission.
	submissions = Submission.objects.filter(enrollment=enrollment, problem=activeProblem).order_by('-date')
	submission = submissions[0] #requires blank submission to be created when a problem is created
	hasPrev = False
	print "Has prev? = " + str(hasPrev)
	if len(submissions) > 1:
		hasPrev = True
	context = Context({"activeProblem": activeProblem, "problems": problems, "submission": submission, "lecture": lecture, "course": course, "user": currentUser, "hasPrev": hasPrev})
	t = get_template("Student.html")
	html = t.render(context)#RequestContext(request, {}))
	return HttpResponse(html)

# An API function that allows a teacher to submit a problem for the students to edit. 
# JSON always returns isOkay and error string.
# If the client only sends a problem_name and lecture_id (blank description) in the POST, then create a problem and 
# return JSON with problem_id. If client POSTs problem_id and description in the POST, then I update the problem. 
# TO IMPLEMENT: when a problem is created, create a blank testcase
def createproblem(request):
	user_id = request.session["user_id"]
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
		if len(problem_name) > 0:
			lecture = Lecture.objects.get(lecture_id=lecture_id)
			newProblemNumber = 0
			allProblems = Problem.objects.filter(lecture=lecture).order_by('-problem_number')
			if len(allProblems) == 0:
				newProblemNumber  = 1
			else:
				newProblemNumber = allProblems[0].problem_number + 1
			newProblem = Problem(name=problem_name, lecture=lecture, problem_number=newProblemNumber)
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
	# Case 2 - problem_id and description
	elif ("problem_id" in request.POST) and ("description" in request.POST):
		problem_id = request.POST["problem_id"]
		description = request.POST["description"]
		if len(description) > 0:
			problem = Problem.objects.get(problem_id=problem_id)
			problem.description = description
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
	user_id = request.session["user_id"]
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
	user_id = request.session["user_id"]
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
			testcaseQuerySet = Testcase.objects.filter(testcase_number=testcase_number)
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
# problem_id, problem_description, name, lecture_id, and solution - from the latest submission. 
# IMPLEMENT: hasPrev
def getproblem(request):
	user_id = request.session["user_id"]
	currentUser = ""
	isOkay = True
	error = ""
	JsonDict = {}
	print request.POST
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	if ("problem_id" in request.POST):
		problem_id = request.POST["problem_id"]
		print "getting problem"
		problem = Problem.objects.get(problem_id=problem_id)
		print "got problem"
		allSubmissions = Submission.objects.filter(problem=problem).order_by('-date')
		print "ordered submissions"
		# Check if there are any matching submissions. If not, create a submission.
		print len(allSubmissions)
		latestSubmission = ""
		if len(allSubmissions) == 0:
			currentEnrollment =  Enrollment.objects.get(user=currentUser, course=problem.lecture.course)
			print currentEnrollment
			latestSubmission = Submission(solution="", enrollment=currentEnrollment, problem=problem, grade=1)
			latestSubmission.save()
		else:
			latestSubmission = allSubmissions[0]
		print "got latest submission"
		print latestSubmission
		JsonDict["problem_id"] = problem_id
		JsonDict["description"] = problem.description
		JsonDict["name"] = problem.name
		#JsonDict["lecture_id"] = problem.lecture.lecture_id
		JsonDict["solution"] = latestSubmission.solution
		JsonDict["submission_id"] = latestSubmission.submission_id
		#HasPrev code#####
		print "JSONified"
		allSubmissionsReordered = allSubmissions.order_by('date')
		print "reordered"
		prevSubmissionIndex = -1
		hasPrev = True
		print range(len(allSubmissionsReordered))
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
	print Json
	return HttpResponse(Json, content_type="application/json")

# Renders the teacher-lecture page with the context vars. 
def teacherlecture(request, lecture_id):
	user_id = request.session["user_id"]
	currentUser = ""
	try:
		currentUser = User.objects.get(user_id=user_id)
	except User.DoesNotExist:
		return HttpResponseRedirect('/')
	lecture = Lecture.objects.get(lecture_id=lecture_id)
	course = lecture.course
	problems = Problem.objects.filter(lecture=lecture_id)
	t = get_template("teacher-lecture.html")
	rc = Context({"user": currentUser, "course": course, "lecture": lecture, "problems": problems})
	html = t.render(rc)#RequestContext(request, {}))
	return HttpResponse(html)

# API function that gets problem_id in POST, returns JSON with problem_description, problem_name
def getproblemteacher(request):
	user_id = request.session["user_id"]
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
	else:
		isOkay = False
		error = post_request_err
	JsonDict["isOkay"] = isOkay
	JsonDict["error"] = error
	Json = simplejson.dumps(JsonDict)
	return HttpResponse(Json, content_type="application/json")

###
# END OF FILE 
###