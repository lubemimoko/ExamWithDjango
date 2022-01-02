from django.shortcuts import get_object_or_404, render, redirect 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .utils import *
from .models import *
from .forms import *



# Create your views here.
#A global scope variable that will be visible in all function
courses = Course.objects.all()

@login_required(login_url='login')
def index(request):
    examCount = Exam.objects.filter(student=request.user).count()
    data={
        "courses": courses, "examCount":examCount
    }
    return render(request, "exam/home.html", data)


@login_required(login_url='login')
def topic(request, id):
    form = TopicForm(c = id)
    
    data = {
        "form":form,
        "courses": courses
    }
    return render(request, "exam/topic.html", data)

@login_required(login_url='login')
def exam(request, urltopic):
   #collect topic, level,course
    if request.method == "POST":
        course= request.POST.get("course")
        topic = request.POST.get("topic")
        level = request.POST.get("level")
        #Fetch question id , insert into exams and redirect to the exams page
        question_ids = []
        
        if request.COOKIES.get("questions"):
            getQuestionIDFromCookies(request)
            return redirect("start_time")
        
        if request.session.get("questions"):
            # return redirect("start_exam")
            pass
        if urltopic.capitalize() == "All":
            qs = Question.objects.values('id').filter(course=course, level=level).order_by('?')[:10]#order by random
            
        else:
            qs = Question.objects.values('id').filter(course=course, topic=topic, level=level).order_by('?')[:10]
           
        for q in qs:
            question_ids.append( q["id"] ) 
              
        request.session["questions"] = question_ids      
        setCookies("questions", question_ids, (60*len(question_ids)) )
        number_of_questions = len(request.session["questions"])
        time_duration = 2 * number_of_questions #in minutes 

        form = ExamForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.student_id = request.user.id
            t.number_of_questions = number_of_questions
            t.time_duration = time_duration
            t.save()
    
            totaltime = totalTime(t.start_time, time_duration)
            request.session["totaltimevalue"] = totaltime 
            request.session["exam"] = t.id 
            
            setCookies("questions", question_ids, (60*len(question_ids)) )

            # return render(request, "exam/home.html")            
            return redirect("start_exam")
    return redirect("home")


@login_required(login_url='login')
def start_exam(request):
    question_ids= request.session.get("questions")
    questions = Question.objects.filter(id__in =question_ids).order_by('?')[:10]#order by random
    
    totaltime = request.session.get("totaltimevalue")
    if not totaltime:
        # totaltime = getTimeFromCookies()
        pass
    data = {"questions":questions, "totaltime":totaltime,
        "courses": courses}
    
    return render(request, "exam/quiz.html", data)


@login_required(login_url='login')
def submit(request):
    questions = request.session.get("questions")
    exam_id = request.session.get("exam")
    
    if not exam_id:
        return redirect("history")
    
    score = 0
    for question in questions:
        
        ans = Answer.objects.values("text").filter(question=question, correct=True)[0]
        
        if ans["text"] == request.POST.get(f'{question}'):
            score +=1
    total_marks = format( (score/len(questions))*100, ".2f" )
    no_ques_attempt = len(request.POST)-1 #CSRF token is also counted by default
    
    Exam.objects.filter(id=exam_id).update(total_marks = total_marks, number_of_questions=len(questions), no_ques_attempt=no_ques_attempt, no_ques_right=score)
    exam = Exam.objects.select_related("topic", "course").filter(id=exam_id).first()
    data = {"total_marks":total_marks, "exam":exam,
        "courses": courses}
    return render(request, "exam/result.html", data)
    
@login_required(login_url='login')
def history(request):
    exams = Exam.objects.select_related("topic", "course").filter(student=request.user.id)
    data = {"exams":exams, "examCount":len(exams),
        "courses": courses}
    return render(request, "exam/history.html", data)
    