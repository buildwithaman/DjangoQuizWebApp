from django.shortcuts import render , HttpResponseRedirect ,redirect
from .forms import RegisterForm , LoginForm , ProfileEditForm , RegisterModelEditForm
from quiz.models import RegisterModel , UserRankModel , QuizSubmissionModel
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate , login , logout 

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        
        profile = User.objects.get(username=request.user)
        user_rank = UserRankModel.objects.order_by('rank')[:4]
        print(user_rank)
        return render(request , 'home.html' ,{'profile':profile ,"user_rank":user_rank} )

    return render(request , 'home.html' )

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = RegisterForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request , "Account Created Successfully")
                return HttpResponseRedirect('/')
                # username = fm.cleaned_data['username']
                # email = fm.cleaned_data['email']
                # password1 = fm.cleaned_data['password1']
                # password2 = fm.cleaned_data['password2']
                # register_user = User
        else:
            fm = RegisterForm()
        return render(request , 'register.html' ,{"form":fm})
    else:
        return redirect('profile' , request.user)

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = LoginForm(request=request , data=request.POST)
            if fm.is_valid():
                username = fm.cleaned_data.get('username')
                password = fm.cleaned_data.get('password')
                account = authenticate(username=username , password=password)
                print(account)
                if account is not None:
                    login(request , account)
                    messages.success(request ,"Logged In Successfully")
                    return redirect('profile' , request.user)
                else:
                    messages.error('Invalid Credentials')
        else:
            fm = LoginForm()
        return render(request , 'signin.html' , {"form":fm})
    else:
        return redirect('profile',request.user)
    
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request , "Logged Out Successfully")
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login/")

def leaderboard(request):
    if request.user.is_authenticated:
        profile = User.objects.get(username=request.user)
        user_rank = UserRankModel.objects.order_by('rank')
        return render(request , 'leaderboard.html' ,{'profile':profile ,"user_rank":user_rank})
    else:
        return HttpResponseRedirect('/signin/')

def editprofile(request):
    if request.user.is_authenticated:
        profile = User.objects.get(username=request.user)
        try:
            register_model_instance = request.user.registermodel
        except RegisterModel.DoesNotExist:
            register_model_instance = None
        if request.method == "POST":
            user_model_form = ProfileEditForm(request.POST , instance=request.user )
            if register_model_instance != None:
                register_model_form = RegisterModelEditForm(request.POST , request.FILES ,instance=request.user.registermodel)
            else:
                register_model_form = RegisterModelEditForm(request.POST , request.FILES)

            # Saving the User model  
            if user_model_form.is_valid():
                user_model_form.save()
            
            # saving the register model form -- if suppose there is no register model for that particular user then it will create a new one then save it to the database and if it exists then it will upadate it
            register_model_instance = register_model_form.save(commit=False)
            
            # print(register_model_instance)
            register_model_instance.user = request.user
            register_model_instance.save()
            messages.success(request , "Profile Updated Successfully")
            return redirect('profile' , request.user)
        else:
            user_model_form = ProfileEditForm(instance=request.user)
            if register_model_instance != None:
                register_model_form = RegisterModelEditForm(instance=request.user.registermodel)
            else:
                register_model_form = RegisterModelEditForm()
        return render(request , 'editprofile.html' , {"user_model_form":user_model_form , "register_model_form":register_model_form  , "profile":profile})
    else:
        return HttpResponseRedirect("/signin/")    

def profile(request , username):
    if request.user.is_authenticated:
        profile = User.objects.get(username=username)
        id = profile.id
        quiz_attended = QuizSubmissionModel.objects.filter(user_id=id)
        print(quiz_attended)
        #total_score = quiz_attended.quiz.questionmodel_set.all().count()*quiz_attended.quiz.pos_marks
        
        return render(request , "profile.html" ,{"profile":profile ,"quiz_attended":quiz_attended })
    else:
        return HttpResponseRedirect('/signin/')
    

def deleteprofile(request):
    if request.user.is_authenticated:
        user_to_delete = User.objects.get(pk=request.user.id)
        user_to_delete.delete()
        messages.success(request ,"Account Deleted Successfully")
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/signin/')