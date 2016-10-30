from django.db import models


# Create your models here.
class Result(models.Model):
    companyShortName = models.CharField(max_length=30)
    companySize = models.CharField(max_length=250)
    positionName = models.CharField(max_length=260)
    salary = models.CharField(max_length=230)
    positionAdvantage = models.CharField(max_length=250)
    workYear = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    education = models.CharField(max_length=30)
    createTime = models.DateField()

    def __str__(self):
        return self.companyShortName


class User(models.Model):
    userName = models.CharField(max_length=20, primary_key=True)
    passWord = models.CharField(max_length=20)
