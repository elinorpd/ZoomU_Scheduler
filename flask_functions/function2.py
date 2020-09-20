

#create a dictionary where each entry is class_name:{dic of its atributes from user input}
user_dic = {}
#create a dictionary where each entry is class_name:{event params from gcal import minus event id}
event_dic = {}
cnt0 = 0
for course in result['items']:
    user_dic[course['summary']]={'sync':course_sync_pref[cnt]}
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
