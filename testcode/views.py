# Shawn Jain
# 1/19/2013
# Testcode project
# views.py

# This file defines the logic to display the page. Methods are 
# invoked automatically when a url is matched in urls.py

#imports
from django.http import HttpResponse

# This is the landing page
def home(request):
	return HttpResponse("My First time on my own!")
