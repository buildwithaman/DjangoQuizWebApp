from django.contrib import admin
from .models import RegisterModel , QuizModel , CategoryModel , QuestionModel , ChoiceModel , UserRankModel , QuizSubmissionModel
# Register your models here.
admin.site.register(RegisterModel)
admin.site.register(QuizModel)
admin.site.register(CategoryModel)
admin.site.register(QuestionModel)
admin.site.register(ChoiceModel)
admin.site.register(QuizSubmissionModel)
admin.site.register(UserRankModel)