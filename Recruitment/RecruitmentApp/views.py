
from os import stat
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser , FormParser, JSONParser
from .models import Applicant, Job, Application
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApplicantSerializer, ApplicationSerializer, JobSerializer
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class ApplicantList(APIView):
    
    parser_classes = ( MultiPartParser, FormParser)

    @swagger_auto_schema()
    def get(self,request):
        """
    List all Applicant Profiles
    ---
    """
        applicant = Applicant.objects.all()
        serializer  = ApplicantSerializer(applicant, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body= ApplicantSerializer )
    def post(self,request):
        """
    Create Applicant Profile
    ---
    """    
        serializer = ApplicantSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class JobList(APIView):

    parser_classes= [JSONParser]

    @swagger_auto_schema() 
    def get(self,request):
        """
    List all Jobs
    ---
    """
        job = Job.objects.all()
        serializer  = JobSerializer(job, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body= JobSerializer )
    def post(self,request):
        """
    Create a new Job Listing
    ---
    """
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
        


class ApplicationList(APIView):
    
    parser_classes= [JSONParser]
    
    @swagger_auto_schema()
    def get(self, request):
        """
    List all applications
    ---
    """
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ApplicationSerializer)
    def post(self, request):
        """
    Create Application   
    ---
    """
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ApplicationDetails(APIView):

    parser_classes = [JSONParser]
    def get_object(self, pk):
        try:
            application = Application.objects.get(id=pk)
            return application
        except :
            raise Http404
    
    @swagger_auto_schema()
    def get(self, request, pk):
        """
    List application by ApplicationID   
    ---
    """
        application = self.get_object(pk)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ApplicationSerializer)    
    def put(self, request, pk):
        """
    Change Appication Status    
    ---
    """
        STAGES = {"PENDING":"REVIEWING","REVIEWING":("SHORTLISTED","REJECTED"),"SHORTLISTED":"INTERVIEWING","INTERVIEWING":("OFFERED","ADVANCE INTERVIEW","REJECTED"),
    "ADVANCE INTERVIEW":("OFFERED","REJECTED"),"OFFERED":("HIRED","REJECTED")}
        application = self.get_object(pk)
        current_stage = ApplicationSerializer(application).data["stage"]
        serializer = ApplicationSerializer(application, data= request.data)
        
        if serializer.is_valid():
            if serializer.validated_data["stage"] in STAGES[current_stage]:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                response_dict = {"Failure":"Cannot change to entered stage, please enter again!! Can only change current status to {}".format(STAGES[current_stage])}
                return Response(data=response_dict)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema()
    def delete(self, request, pk):
        """
    Delete Appication     
    ---
    """
        application = self.get_object(pk)
        application.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)