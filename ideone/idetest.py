# Shawn Jain
# 1/29/2013
# Testcode Project

# idetest.py

from ideone import *

ideone = IdeOne()

# run a python program
python = 116

link = ideone.createSubmission("print 'Hello World!!", python)

# wait for it to finish 
while ideone.getSubmissionStatus(link)[0] != Status.Done:
    pass

# print output
print ideone.getSubmissionDetails(link)['output']