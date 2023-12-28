from django.shortcuts import render , HttpResponseRedirect ,redirect
from .models import QuizModel , CategoryModel , QuestionModel ,QuizSubmissionModel
from django.db.models import Q
from django.contrib import messages
from .forms import QuizForm
# Create your views here.
def allquiz(request):
    
    if request.user.is_authenticated:
        categories = CategoryModel.objects.all()
        quizzes = QuizModel.objects.all()
        return render(request , "allquiz.html" ,{"quizzes" : quizzes , "categories":categories})
    else:
        return HttpResponseRedirect('/signin/')
    
def search(request , category_name):
    
    if category_name == " ":
        quizzes = QuizModel.objects.all()
    elif request.GET.get('q') != None:
        q = request.GET.get('q')
        quizzes = QuizModel.objects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(created_by__username__icontains=q) | Q(created_by__first_name__icontains=q) | Q(created_by__last_name__icontains=q))
    else:
        quizzes = QuizModel.objects.filter(categories__category_name=category_name)
    categories = CategoryModel.objects.all()
    return render(request , 'allquiz.html' ,{"quizzes":quizzes ,"categories":categories})


def quiz(request , id):
    if request.user.is_authenticated:
        # quiz = QuizModel.objects.get(pk=id)
        quiz = QuizModel.objects.filter(id=id).first()

        correct_ans = QuestionModel.objects.values('id' ,'question_text' , 'choicemodel__is_correct')
        
        total_score = quiz.questionmodel_set.all().count()*quiz.pos_marks
        
        
        # print("get ",QuizModel.objects.get(pk=1))
        # print("filter ",QuizModel.objects.filter(id=1))
        h = int(str(quiz.quiz_duration)[:2])

        m = int(str(quiz.quiz_duration)[3:5])
        

        if request.method == "POST":
            score = int(request.POST.get('score' ,18))
            print("Score" , score)

            # check if the user has already submitted the quiz
            if QuizSubmissionModel.objects.filter(user=request.user , quiz=quiz).exists():
                messages.success(request , f'This time You have Scored {score} out of {total_score}')
                return redirect('quiz' , id)
            
            # save the new quiz submission
            submission = QuizSubmissionModel(user=request.user , quiz=quiz , score=score)
            submission.save()
            messages.success(request , f"New Submission Made , You have Scored {score} out of {total_score}")    
            return redirect('quiz' ,id )

        return render(request , 'quiz.html' , {"quiz":quiz, "hour":h , "min":m ,"correct_ans":correct_ans})
    else:
        return HttpResponseRedirect('/signin/')
    

def addquiz(request):
    if request.method == "POST":
        fm = QuizForm(request.POST , request.FILES)
        if fm.is_valid():
            title = fm.cleaned_data.get('title')
            desc = fm.cleaned_data.get('description')
            cat = fm.cleaned_data.get('categories')
            quiz_file =fm.cleaned_data.get('quiz_file')
            # fm.cleaned_data.get('created_by')
            duration = fm.cleaned_data.get('quiz_duration')
            pos_marks = fm.cleaned_data.get('pos_marks')
            neg_marks = fm.cleaned_data.get('neg_marks')
            new_quiz = QuizModel(title=title , description=desc , quiz_file= quiz_file , created_by=request.user ,quiz_duration=duration , pos_marks=pos_marks , neg_marks = neg_marks) 
            new_quiz.save()
            new_quiz.categories.set(cat)
            new_quiz.save()
            messages.success(request , "New Quiz Added Sucessfully")
            return HttpResponseRedirect('/allquiz/')
    else:
        fm = QuizForm()
    return render(request , "addquiz.html" ,{"form":fm})