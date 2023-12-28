from django import forms
from .models import QuizModel , CategoryModel
from django.core.validators import FileExtensionValidator

class QuizForm(forms.ModelForm):
    quiz_file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])],
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=CategoryModel.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input" ,"type":"checkbox"}),
    )
    quiz_duration = forms.TimeField(
        widget=forms.TimeInput(attrs={"type":"time"}),
        required=True
    )
    pos_marks = forms.IntegerField(
        required=True,
    )
    neg_marks = forms.IntegerField(
        required=True,  
    )
    class Meta:
        model = QuizModel
        exclude = ['updated_at' , 'created_at' , 'created_by' ]
        widgets={
            'title':forms.TextInput(attrs={"class":"form-control"}),
            'description':forms.Textarea(attrs={"class":"form-control"}),
            # 'categories':forms.MultipleChoiceField(attrs={"class":"form-select"}),
            # 'quiz_file':forms.FileInput(attrs={"class":"form-control"}),
            # 'quiz_duration':forms.TimeInput(attrs={"class":"form-control" , "type":"time"}),
            'pos_marks':forms.NumberInput(attrs={"class":"form-control"}),
            'neg_marks':forms.NumberInput(attrs={"class":"form-control"}),
            # 'created_by':forms.Select(attrs={"class":"form-select"}),
            
        }