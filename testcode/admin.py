# Shawn Jain
# Jan 22 2013
# Testcode project
# admin.py

# Register the models for the admin database

# imports
from django.contrib import admin
from testcode.models import *

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Problem)
admin.site.register(Testcase)
admin.site.register(Enrollment)
admin.site.register(Submission)
