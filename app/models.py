from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=13)
    isComing = models.BooleanField()
    def __str__(self):
        return self.name

class Lecture(models.Model):
    subject = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    hash = models.CharField(max_length=500)
    def __str__(self):
        return "Lecture %s" % self.subject

class Homework(models.Model):
    subject = models.CharField(max_length=20)
    issue_date = models.DateField()
    submission_date = models.DateField()
    task_text = models.CharField(max_length=500)
    hash = models.CharField(max_length=500)
    def __str__(self):
        return "Homework %s, %s, %s" % (self.subject, self.issue_date.__str__(), self.submission_date.__str__())

class Meeting(models.Model):
    place = models.CharField(max_length=100)
    date = models.DateField()
    description = models.CharField(max_length=500)
    def __str__(self):
        return "Meeting at %s, at %s" % (self.place, self.date.__str__())

class CustomFile(models.Model):
    file_name = models.CharField(max_length=50)
    file_source = models.CharField(max_length=500)
    hash = models.CharField(max_length=500)
    def __str__(self):
        return self.file_name

class ImportantInfo(models.Model):
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=1000)
    date = models.DateField()
    hash = models.CharField(max_length=500)
