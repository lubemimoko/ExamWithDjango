from django.contrib import admin
from  .models import Student, Course, Exam, Topic, Question, Answer, Result

# Register your models here.
admin.site.site_header = "ONLINE EXAMINATION SYSTEM"
admin.site.index_title = "Exam's Administration"
admin.site.index_title = "Aptech Admins"
admin.site.site_title = "ONLINE EXAM DASHBOARD"


class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]    


admin.site.register(Student)
# admin.site.register(Exam)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)
