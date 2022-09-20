from random import choices
from django.db import models
from django.forms import ChoiceField

# Create your models here.

class Applicant(models.Model):
    applicant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    resume = models.FileField(upload_to='staticfiles/resumes/')
    

class Job(models.Model):
    applicant = models.ManyToManyField(Applicant, through='Application')
    job_id = models.AutoField(primary_key=True)
    job_description = models.TextField()

class Application(models.Model):
    status_choices = (("PENDING","PENDING"),("REVIEWING","REVIEWING"), ("SHORTLISTED","SHORTLISTED"),("REJECTED","REJECTED"),("INTERVIEWING","INTERVIEWING"),("ADVANCE INTERVIEW","ADVANCE INTERVIEW"),
    ("OFFERED","OFFERED"), ("HIRED","HIRED"))
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job  = models.ForeignKey(Job, on_delete=models.CASCADE) 
    stage = models.TextField(choices=status_choices, default="PENDING")

    class Meta:
        unique_together = ('applicant', 'job')








    


    
