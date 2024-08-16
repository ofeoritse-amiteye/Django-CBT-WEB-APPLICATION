from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ACCOUNT_TYPE = [
        ('admin', 'Admin'),
        ('it_user', 'it_user'),
        ('staff', 'staff'),
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE,)
    email = models.CharField(max_length=100)
    phone=models.CharField(max_length=100 , default="")
    last_login=models.CharField(max_length=100 ,default="")
    password =models.CharField(max_length=100,default="CBTUSER1234")

    def __str__(self):
        return self.username
    
class questions(models.Model):
    question_no=models.CharField(max_length=100,default="none")
    category=models.CharField(max_length=100)
    question=models.TextField()
    answer=models.TextField()
    opt_a=models.CharField(max_length=100)
    opt_b=models.CharField(max_length=100)
    opt_c=models.CharField(max_length=100)
    opt_d=models.CharField(max_length=100)
    
    
    
    class Meta:
        db_table = 'questions'
        
        
class test(models.Model):
    title=models.CharField(max_length=100 ,default="none")
    category=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    participant=models.CharField(max_length=100)
    
    class Meta:
        db_table = 'test'
        
class user_score(models.Model):
    Name=models.CharField(max_length=100)
    user=models.CharField(max_length=100)
    score=models.CharField(max_length=100)
    test=models.CharField(max_length=100 , default="none")
    grade=models.CharField(max_length=100, default="NONe")
    class Meta:
        db_table = 'test_scores'
        
