# ZoomU Academic Scheduler

## The perfect tool to help you balance your remote courses and academic work schedule.

This was created as a submission to HackMIT 2020 in the Education track.

Our tool takes in a Google calendar of the user’s classes, local timezone, the timezone of their school, and some information about the synchronicity of the classes, mandatory attendance, and the user’s preferences on when and how to learn. Our tool would then create an adjusted schedule that marks the best times to view asynchronous lectures and work on homework, based off of the user’s timezone, local daylight hours, and the user’s preferences; and return that schedule as a new Google calendar.

It's not perfect, but the basic functionality is there for a project developed in less than 36 hours by two new hackers :).

## Running the webapp locally

1. Download all the files

2. From the ZoomU_Scheduler directory, run run.py

	`python run.py`
3. Navigate to http://localhost:5000 in your browser and click on 'Click HERE to get started'

4. Login to your Google account and follow authentication instructions to allow access to your Google Calendar.

	If you get a 'This app isn't verified' warning, click on 'Advanced' and then 'Go to Quickstart (unsafe)'

5. Enter the number of the calendar you would like to use -1 (they are indexed starting from 0 - needs to be fixed)

6. Authenticate again (same as #4)

7. Fill out the webform and make sure to check the Confirm button before sumbitting.

8. Authenticate again (same as #4)

9. Click the link to view your new calendar or reload Google Calendar in another tab! It has been automatically added to your Google Calendar.

Use `CTRL+C` to quit. 


## Important files and folders overview
1. workbook.ipynb is the original python script that will run on it's own, unrelated to the web app.

2. app/ contains the necessary files to run the web application, including the template and static folders with the html and css files respectively.

3. flask_functions/ contains python files adapted from workbook.ipynb for ease in adding to the webapp, they don't actually run on their own.

4. masha_credentials.json contains API key info for the Google Calendar authentification.

5. run.py is the python script that will run the webapp.
