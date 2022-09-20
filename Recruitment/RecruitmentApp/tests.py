import email
import os
from urllib import response
from django.test import Client
from rest_framework import  status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from sqlalchemy import JSON

from RecruitmentApp.serializers import ApplicantSerializer, ApplicationSerializer, JobSerializer
from .models import Applicant, Application, Job
# Create your tests here.


class ApplicantListTest(APITestCase):

    def tearDown(self):
        os.remove("resumes/Test_resume.pdf")

    def test_get(self):
        file_field = SimpleUploadedFile('Test_resume.pdf', b'these are the contents of the pdf file')
        Applicant.objects.create(name="Test User",email="testemail@email.com",resume=file_field)
        c = Client()
        response = c.get("/Applicants/")
        applicant = Applicant.objects.all()
        applicant.delete()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_post(self):
        c = Client()
        file_field = SimpleUploadedFile('Test_resume.pdf', b'these are the contents of the pdf file')
        data = {"name":"Test New Name", "email": "testemail@email.com", "resume": file_field}
        response = c.post("/Applicants/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        applicant = Applicant.objects.all()
        applicant.delete()

class JobListTest(APITestCase):

     def test_get(self):
        c= Client()
        Job.objects.create(job_description="Software Developer")
        response = c.get("/Job/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        jobs = Job.objects.all()
        jobs.delete()

     def test_post(self):
        c = Client()
        data = {"job_description":"Software Developer"}
        response =  c.post("/Job/", data=data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        jobs = Job.objects.all()
        jobs.delete()

class ApplicationListTest(APITestCase):

    def tearDown(self):
        os.remove("resumes/Test_resume.pdf")
        applicant = Applicant.objects.all()
        applicant.delete()
        job = Job.objects.all()
        job.delete()
        application = Application.objects.all()
        application.delete()
        

    def test_get(self):
        c = Client()
        file_field = SimpleUploadedFile('Test_resume.pdf', b'these are the contents of the pdf file')
        Applicant.objects.create(name="Test User",email="testemail@email.com",resume=file_field)
        applicant_id = ApplicantSerializer(Applicant.objects.get(name="Test User")).data['applicant_id']
        Job.objects.create(job_description="Software Developer")
        job_id =  JobSerializer(Job.objects.get(job_description="Software Developer")).data['job_id']
        Application.objects.create(job_id=job_id, applicant_id=applicant_id)
        response = c.get("/Applications/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
    def test_post(self):
        c = Client()
        file_field = SimpleUploadedFile('Test_resume.pdf', b'these are the contents of the pdf file')
        Applicant.objects.create(name="Test User",email="testemail@email.com",resume=file_field)
        applicant_id = ApplicantSerializer(Applicant.objects.get(name="Test User")).data['applicant_id']
        Job.objects.create(job_description="Software Developer")
        job_id =  JobSerializer(Job.objects.get(job_description="Software Developer")).data['job_id']
        data = {"applicant":applicant_id, "job":job_id}
        response = c.post("/Applications/", data=data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class ApplicationDetailsTest(APITestCase):

    def setUp(self) :
        self.c = Client()
        self.file_field = SimpleUploadedFile('Test_resume.pdf', b'these are the contents of the pdf file')
        Applicant.objects.create(name="Test User",email="testemail@email.com",resume=self.file_field)
        self.applicant_id = ApplicantSerializer(Applicant.objects.get(name="Test User")).data['applicant_id']
        Job.objects.create(job_description="Software Developer")
        self.job_id =  JobSerializer(Job.objects.get(job_description="Software Developer")).data['job_id']
        Application.objects.create(job_id=self.job_id, applicant_id=self.applicant_id)
        self.application_id = ApplicationSerializer(Application.objects.get(applicant=self.applicant_id)).data['id']
        
    def tearDown(self):
        os.remove("resumes/Test_resume.pdf")
        applicant = Applicant.objects.all()
        applicant.delete()
        job = Job.objects.all()
        job.delete()
        application = Application.objects.all()
        application.delete()

    def test_get(self):
        response = self.c.get("/Applications/{}".format(self.application_id))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_put(self):
        data = {'id':self.application_id, "stage":"REVIEWING",'applicant':self.applicant_id,'job':self.job_id}
        response  = self.c.put("/Applications/{}".format(self.application_id), data=data,content_type='application/json' )  
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    
    def test_delete(self):
        response= self.c.delete("/Applications/{}".format(self.application_id))
        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)

