from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
import pandas as pd
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

gender_choices = [
    ('Male' , 'Male'),
    ('Female','Female'),
    ('Others','Others')
]
# Create your models here.
class RegisterModel(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , null=True , blank=True)
    bio = models.TextField(max_length=255 ,null=True , blank=True)
    gender = models.CharField(choices=gender_choices ,max_length=6 ,null=True , blank=True)
    profile_img = models.ImageField(upload_to="profile_images" , default="profile_images/userprofile.png" ,null=True , blank=True)
    college_name = models.CharField(max_length=80 , null=True , blank=True , default="Not Available")

    def __str__(self):
        return self.user.username
    
class CategoryModel(models.Model):
    category_name = models.CharField(max_length=25)
    def __str__(self):
        return self.category_name

class QuizModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(CategoryModel)
    quiz_file = models.FileField(upload_to='quiz_file' , null=True ,blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL , null=True ,blank=True)
    quiz_duration = models.TimeField(null=True , blank=True)
    pos_marks = models.IntegerField(null=True , blank=True)
    neg_marks = models.IntegerField(null=True , blank=True)

    def __str__(self):
        return self.title
    
    # this function is called when we save the quiz
    def save(self, *args ,**kwargs):
        super().save(*args, **kwargs)
        if self.quiz_file:
            self.import_quiz_from_excel()
    
    # this function import the quiz , choices from the excel sheet
    def import_quiz_from_excel(self):
            df = pd.read_excel(self.quiz_file.path)
            for index , row in df.iterrows():
                question_text = row['Question']
                choice1 = row['A']
                choice2 = row['B']
                choice3 = row['C']
                choice4 = row['D']
                correct_ans = row['Answer']
                print(index)

                # creating question object
                question = QuestionModel.objects.get_or_create(quiz=self , question_text=question_text)

                # creating choice object
                choice_1 = ChoiceModel.objects.get_or_create(question=question[0] , choice_text=choice1 , is_correct=correct_ans=='A')
                choice_2 = ChoiceModel.objects.get_or_create(question=question[0] , choice_text=choice2 , is_correct=correct_ans=='B')
                choice_3 = ChoiceModel.objects.get_or_create(question=question[0] , choice_text=choice3 , is_correct=correct_ans=='C')
                choice_4 = ChoiceModel.objects.get_or_create(question=question[0] , choice_text=choice4 , is_correct=correct_ans=='D')
                
    
class QuestionModel(models.Model):
    quiz = models.ForeignKey(QuizModel , on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text[:50]


class ChoiceModel(models.Model):
    question = models.ForeignKey(QuestionModel , on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text[:20]


class QuizSubmissionModel(models.Model):
    quiz = models.ForeignKey(QuizModel , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quiz.title}  {self.user.username}'
    
class UserRankModel(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    rank = models.IntegerField(null=True,blank=True)
    total_score = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f'{self.user.username}  {self.rank}'

@receiver(post_save , sender=QuizSubmissionModel)
def update_leaderboard(sender , instance , created ,**kwargs):
    if created:
        update_leaderboard()

def update_leaderboard():
    # calculate the total score of the user
    user_score = QuizSubmissionModel.objects.values('user').annotate(total_score=Sum('score')).order_by('-total_score')
    print("user_score ",user_score)

    # update rank based on the sorted list of dictionary
    rank = 1 
    for entry in user_score:
        user_id = entry['user']
        total_score = entry['total_score']

        user_rank , created = UserRankModel.objects.get_or_create(user_id=user_id)
        user_rank.rank = rank
        user_rank.total_score = total_score
        user_rank.save()
        rank +=1