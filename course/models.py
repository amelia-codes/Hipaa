from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#from django.db import models
class Ques(models.Model):
    question = models.CharField(max_length = 500) #check if null True by default
    option1 = models.CharField(max_length = 500)
    option2 = models.CharField(max_length = 500)
    option3 = models.CharField(max_length = 500)
    option4 = models.CharField(max_length = 500)
    correctanswer = models.CharField(max_length = 500)

class ValidUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    email=models.CharField(max_length=255)
    score=models.IntegerField(default=0)
    progress=models.IntegerField(default=0)
    name=models.CharField(max_length=225)
    attempt=models.IntegerField(default=0)
    awknowledge=models.BooleanField(default=False)
    

