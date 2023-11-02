from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    Passed_Tests = models.PositiveIntegerField(default=0)
    Correct_Answers = models.PositiveIntegerField(default=0)
    Wrong_Answers = models.PositiveIntegerField(default=0)
    Perfect_Tests = models.PositiveIntegerField(default=0)
    Successes_Rate = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        try:
            self.Successes_Rate = self.Correct_Answers / (self.Correct_Answers + self.Wrong_Answers)
        except ZeroDivisionError:
            self.Successes_Rate = 0
        return super(User, self).save(*args, **kwargs)


class Question(models.Model):
    image = models.ImageField(upload_to='images/')
    right_answer = models.CharField(max_length=256)
    wrong_answer_1 = models.CharField(max_length=256)
    wrong_answer_2 = models.CharField(max_length=256)
    wrong_answer_3 = models.CharField(max_length=256)
    wrong_answer_4 = models.CharField(max_length=256)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
