from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm ,UsernameField , UserChangeForm
from django.utils.translation import gettext , gettext_lazy as _
from quiz.models import RegisterModel

gender_choices =[
    ('male' , 'male'),
    ('female','female'),
    ('others','others')
]

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}) , label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {"class":"form-control"}), label="Confirm Password" ) 
    email = forms.EmailField(required=True , widget=forms.EmailInput(attrs={"class":"form-control"}))
    class Meta:
        model = User
        fields = ['username' , 'email']
        widgets = {
            'username':forms.TextInput(attrs={"class":"form-control"}),
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True , "class":"form-control"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password" , "class":"form-control"}),
    )

class ProfileEditForm2(UserChangeForm):
    password = None
    bio=forms.CharField(max_length=255 , required=True , widget=forms.TimeInput(attrs={"class":"form-control"}))
    gender=forms.ChoiceField(choices=gender_choices , widget=forms.Select(attrs={"class":"form-select"}))
    college_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_img = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ['first_name' , 'last_name' ,'bio' , 'gender' ,'college_name' , 'profile_img']
        widgets={
            'first_name':forms.TextInput(attrs={"class":"form-control"}),
            'last_name':forms.TextInput(attrs={"class":"form-control"})

            }
    
    def __init__(self, *args, **kwargs):
        register_model_instance = kwargs.pop('register_model_instance', None)
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # You can customize the labels or widgets if needed
        self.fields['bio'].label = 'Bio'
        self.fields['gender'].label = 'Gender'
        self.fields['college_name'].label = 'College Name'
        self.fields['profile_img'].label = 'Profile Image'

class ProfileEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields=['first_name' , 'last_name' , 'email']
        widgets={
            'first_name':forms.TextInput(attrs={"class":"form-control"}),
            'last_name':forms.TextInput(attrs={"class":"form-control"}),
            'email':forms.EmailInput(attrs={"class":"form-control"})
            }

class RegisterModelEditForm(forms.ModelForm):
    # gender = forms.ChoiceField(choices=gender_choices , widget=forms.Select(attrs={"class":"form-"}))
    class Meta:
        model =RegisterModel
        fields =['bio' , 'profile_img' , 'gender' , 'college_name']
        widgets={
            'bio':forms.TextInput(attrs={"class":"form-control"}),
            'profile_img':forms.FileInput(attrs={"class":"form-control"}),
            'gender':forms.Select(attrs={"class":"form-select"}),
            'college_name':forms.TextInput(attrs={"class":"form-control"}),
            
        }