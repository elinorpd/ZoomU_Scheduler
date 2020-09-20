from  __future__  import print_function
from flask import Flask, render_template, request, redirect, flash, url_for
from app import app
from app.forms import LoginForm
import datetime
import pickle
import os.path
import googleapiclient.discovery
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime as dt
import pytz
import copy




@app.route('/')
@app.route('/index')
def index():
    #print("hello world")
	user = {'username': 'Elinor'}
	posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
	return render_template('index.html', title="corndog", user=user, posts=posts)

@app.route("/cal")
def cal():
    creds =  None
    SCOPES  = ['https://www.googleapis.com/auth/calendar.readonly']
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    flow = InstalledAppFlow.from_client_secrets_file(
    'masha_credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            # with open('token.pickle', 'wb') as token: # can't write files in Google App Engine so comment out or delete
            # pickle.dump(creds, token)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    # Call the Calendar API

    #mashas code
    print('listing all calendars')
    cal_result = service.calendarList().list().execute()
    print(cal_result['items'])
    cnt = 0
    calendar_list = []
    for i in cal_result['items']:
        calendar_list.append(i['summary'])
    for i in calendar_list:
        print(cnt, i)
        cnt +=1
    

    return  render_template("cal.html", calendar_list=calendar_list)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    calendar_choice = int(request.form['gcalnum'])

    creds =  None
    SCOPES  = ['https://www.googleapis.com/auth/calendar.readonly']
    flow = InstalledAppFlow.from_client_secrets_file('masha_credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    cal_result = service.calendarList().list().execute()
    calendar_id = cal_result['items'][calendar_choice]['id']
    result = service.events().list(calendarId=calendar_id).execute()

    course_list = []
    for course in result['items']:
        course_list.append(course['summary'])
    print(course_list)    


    return render_template('schedule.html', calendar_choice=calendar_choice, course_list=course_list)

@app.route('/creating', methods=['GET', 'POST'])
def creating():
    calendar_choice = int(request.form['calendar_choice'])
    sleep_time = int(request.form['sleep'])
    time_of_day = int(request.form['studypref'])
    localtimezone= "UTC"+request.form['localtimezone']
    schooltimezone= "UTC"+request.form['schooltimezone']


    creds =  None
    SCOPES  = ['https://www.googleapis.com/auth/calendar.readonly']
    flow = InstalledAppFlow.from_client_secrets_file('masha_credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    cal_result = service.calendarList().list().execute()
    calendar_id = cal_result['items'][calendar_choice]['id']
    result = service.events().list(calendarId=calendar_id).execute()

    course_list = []
    for course in result['items']:
        course_list.append(course['summary'])

    course_sync_pref = [int(request.form['course1']),int(request.form['course2']), int(request.form['course3']), int(request.form['course4']), int(request.form['course5'])]
    #create a dictionary where each entry is class_name:{dic of its atributes from user input}
    user_dic = {}
    #create a dictionary where each entry is class_name:{event params from gcal import minus event id}
    event_dic = {}
    cnt0 = 0
    for course in result['items']:
        if cnt0 >= 5:
            break
        user_dic[course['summary']]={'sync':course_sync_pref[cnt0]}
        event_dic[course['summary']]= copy.deepcopy(course)
        cnt0 += 1
        try:
            del event_dic[course['summary']]['id']#remove the event id bc that's specific to this calendar and i just need the event parameters
            del event_dic[course['summary']]['htmlLink']
            del event_dic[course['summary']]['iCalUID']
            del event_dic[course['summary']]['etag']
            del event_dic[course['summary']]['organizer']
            del event_dic[course['summary']]['recurringEventId']
        except KeyError:
            pass
        except:
            break
        #create a new calendar, and then we'll add events to it directly
    home_tz = pytz.timezone('Europe/Moscow') #switch to user input later
    newcalendar = {'summary': 'new_test_calendar','timeZone': 'Europe/Moscow'} #need to change cal name lol

    created_calendar = service.calendars().insert(body=newcalendar).execute()

    new_calendar_id = created_calendar['id']

    school_tz = pytz.timezone('America/New_York')


    #first, sort the events by synchronicity
    synch = [course[0] for course in user_dic.items() if course[1]['sync']==2]
    semisynch = [course[0] for course in user_dic.items() if course[1]['sync']==1]
    asynch = [course[0] for course in user_dic.items() if course[1]['sync']==0]




    #first, create the events for the completely synchronous classes
    for name in synch:
        print(name)
        service.events().insert(calendarId=new_calendar_id, body=event_dic[name]).execute()

    def freebusy():
        dt1 = home_tz.localize(dt(2020, 9, 21, 12))
        dt2 = home_tz.localize(dt(2020, 9, 22, 12))
        body = {"kind":"calendar#freeBusy",
          "timeMin": dt1.isoformat(), # in future need tp have it do next monday to next sunday
          "timeMax": dt2.isoformat(),
          "timeZone": 'Europe/Moscow',
          "items": [
            {
              "id": new_calendar_id
            }
          ]
        }

        free = service.freebusy().query(body=body).execute()
        return free

        free = freebusy()

    #next, set a sleep time

    times_list = []
    class_starts = []
    class_ends = []
    for dic in free['calendars'][new_calendar_id]['busy']:
        print(dic)
        #get the intervals as datetime
        times_list.append(dic['start'])
        class_starts.append(dic['start'])
        times_list.append(dic['end'])
        class_ends.append(dic['end'])

    times_list.sort()
    times_list = [dt.strptime(time[0:-6],'%Y-%m-%dT%H:%M:%S') for time in times_list]
    #class_starts = [dt.strptime(time[0:-6],'%Y-%m-%dT%H:%M:%S') for time in class_starts]
    #class_ends = [dt.strptime(time[0:-6],'%Y-%m-%dT%H:%M:%S') for time in class_ends]
    class_starts = [int(time[11:13]) for time in class_starts]
    class_ends = [int(time[11:13]) for time in class_ends]

    try:
        latest_class = max(i for i in class_ends if i <= 5)
    except:
        latest_class = max(class_ends)

    earliest_class = min(i for i in class_starts if i >= 5)


    def make_sleep_event():
        event = { #need to add recurrence!
              'summary': 'Sleept',
              'description': 'zzzzzz',
            'recurrence': ['RRULE:FREQ=DAILY'],
              'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'Europe/Moscow',
              },
              'end': {
                'dateTime': stop_datetime.isoformat(),
                'timeZone': 'Europe/Moscow',
              }
            }
        event = service.events().insert(calendarId=new_calendar_id, body=event).execute()

    if time_of_day == 0: #if morning person
        #find the sleep start time that's 10 pm or 1 hr after your last class, whichever is earlier
        if latest_class <= 21 and latest_class >= 12:
            #sleep at 22
            start_datetime = dt(2020, 9, 21, 22)
            stop_datetime = dt(2020, 9, 22, (22+sleep_time)%24)
            make_sleep_event()
        else:
            #sleep at latest_class+1
            if latest_class <= 5:
                start_datetime = dt(2020, 9, 22, latest_class+1) #this would be so much easier achieved w datetimes ngl
            else:
                start_datetime = dt(2020, 9, 21, latest_class+1)
            stop_datetime = dt(2020, 9, 22, (latest_class+1+sleep_time)%24)
            make_sleep_event()
    else: #if night owl
        #find the sleep start that ends at 12 pm or an hour before earliest class, whichever is later
        if earliest_class >= 13:
            #sleep until 12
            start_datetime = dt(2020, 9, 22, 12-sleep_time)
            stop_datetime = dt(2020, 9, 22, 12)
            make_sleep_event()
        else:
            start_datetime = dt(2020, 9, 22, earliest_class-1-sleep_time)
            stop_datetime = dt(2020, 9, 22, earliest_class-1)
            make_sleep_event()

    for name in semisynch:
        print(name)
        print(event_dic[name]['start'], event_dic[name]['end'])
        start_time = str(event_dic[name]['start']['dateTime'])[11:16]
        end_time = str(event_dic[name]['end']['dateTime'])[11:16]

        free = {}
        we_good = True
        for i in range(21,22):
            #test that yuo're not busy any day at that time
            dt1 = school_tz.localize(dt(2020, 9, i, int(start_time[0:2]), int(start_time[3:5])))
            dt2 = school_tz.localize(dt(2020, 9, i, int(end_time[0:2]), int(end_time[3:5])))
            print(dt1,dt2)
            body = {"kind":"calendar#freeBusy",
              "timeMin": dt1.isoformat(), #need tp have it do next monday to next sunday
              "timeMax": dt2.isoformat(),
              "timeZone": 'America/New_York',
              "items": [
                {
                  "id": new_calendar_id
                }
              ]
            }

            free = service.freebusy().query(body=body).execute()

            if not free['calendars'][new_calendar_id]['busy']==[]:
                asynch.append(name)
                we_good = False
                break

        if we_good:
            service.events().insert(calendarId=new_calendar_id, body=event_dic[name]).execute()


    return render_template('creating.html')


