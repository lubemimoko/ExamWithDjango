from django.forms import ModelForm
from .models import *


class TopicForm(ModelForm):
    class Meta:
            model = Exam
            fields=("course", "topic", "level")

        
    def __init__(self, c, *a, **b):  

        super(TopicForm, self).__init__( *a, **b)
        self.fields["course"].queryset = Course.objects.filter(id=c)
        self.fields["topic"].queryset = Topic.objects.filter(course=c)
        
    


class ExamForm(ModelForm):
    class Meta:
            model = Exam
            fields=("course", "topic", "level")

    


