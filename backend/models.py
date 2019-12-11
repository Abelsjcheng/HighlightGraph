from django.db import models

# Create your models here.


class Username(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    sex = models.CharField(max_length= 10)
    age = models.IntegerField()
    education = models.CharField(max_length=20)
    research = models.CharField(max_length=100)
    background = models.IntegerField(default=1)


class Duration(models.Model):
    did = models.AutoField(primary_key=True)
    time = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    consumingtime = models.IntegerField()
    username = models.ForeignKey('Username', on_delete=models.CASCADE, default='')


class Rectangle(models.Model):
    rid = models.AutoField(primary_key=True)
    time = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()
    username = models.ForeignKey('Username', on_delete=models.CASCADE, default='')
    duration = models.ForeignKey('Duration', on_delete=models.CASCADE, default='')


class Questions(models.Model):
    qid = models.CharField(max_length=50, primary_key=True)
    type = models.IntegerField()
    name = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    choices = models.CharField(max_length=255, null=True)
    questionImg = models.CharField(max_length=50, blank=True, null=True)
    background = models.IntegerField(default=0)
    TestType = models.IntegerField(default=1)


class Background(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    background = models.TextField()
    label = models.TextField(blank=True, null=True)
    graphname = models.CharField(max_length=50, null=True)


class Answers(models.Model):
    rid = models.AutoField(primary_key=True)
    time = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    x1 = models.FloatField(blank=True, null=True)
    y1 = models.FloatField(blank=True, null=True)
    x2 = models.FloatField(blank=True, null=True)
    y2 = models.FloatField(blank=True, null=True)
    consumingtime = models.FloatField(default=0)
    answer = models.CharField(max_length=255, blank=True, null=True)
    TestType = models.IntegerField(default=1)
    qid = models.ForeignKey('Questions', on_delete=models.CASCADE, default='')
    username = models.ForeignKey('Username', on_delete=models.CASCADE, default='')
#     def __str__(self):
#         return "{" + "name: {0}, x1: {1}, y1: {2}, x2: {3}, y2: {4}".format(self.name, self.x1, self.y1, self.x2, self.y2) + "}"