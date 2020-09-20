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
 
