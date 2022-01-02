from django.http.response import HttpResponse


def timevalue(datetime, array=True):
    datetime = str(datetime)
    if datetime.find(" ") > 0:
        time = datetime.split(" ")[1]
    else:
        time = datetime
    time = time.split(":")
    hr = int(time[0]) *3600
    min = int(time[1]) * 60
    sec = int(time[2].split(".")[0])
    return hr + min + sec
    
def compareTime(time1, time2):
    time1 = time1.strip() 
    time2 = time2.strip()        
    
    value1 = timevalue(time1)    
    value2 = timevalue(time2)        
    return value2 - value1

def totalTime(time, duration): 
    return timevalue(time) + (duration*60)   

def getTimeFromCookies(): 
    pass

def getQuestionIDFromCookies(request):
    request.session["questions"] = list(request.COOKIES.get("questions"))


def setCookies(cookie, value, exp):

    res = HttpResponse("Cookie o") 
    res.set_cookie("cookie", value, max_age=exp ) 
    return res















    