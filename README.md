# RecruitmentPipeline

Approach:

Backend: The backend consists of APIs built using the Django Rest Framework. There are APIs for creating Applicant profiles by entering name, email ID and
resume of the applicant. Similarly, by entering just the Job Description, a job listing can be created. These are auxilary functions and therefore only basic
GET and POST are implemented for this. However, the main functionality of the API is to create Applications by entering the Job ID and Applicant ID 
(easily available to view) and change the status of an Application. At the time of creation of a new application, the stage is automatically set to PENDING. 
Checks are provided to ensure that no other stage can be set at the time of creation. Once an Application is created, the user/recruitter can change the 
application stage as per the business logic. Again, the business logic has been implemented in the appropriate view to ensure that only certain stages can 
be reached from the current stage. If the recruiter tries to change the current stage to a stage that isn't permissible per the business logic, the API 
returns the appropriate response guiding the user to the stages that are avaialble to him.

FrontEnd: The frontend has been kept light, and in a standard template for APIs, by using the Swagger Open API. It is easy to integrate with Django, and it
is also easy to use. The user can browse on all actions available while also being able to see example model values that are needed for every action. Each 
action expects data in the JSON format, which is easily readable by humans and machine alike.

Models: There are 3 models, namely Job, Applicant and Application. The Job and Applicant models are provided to ensure the creation of job lisitngs and 
applicant profiles. There is only limited actions avaialble on these models, since this is not the prupose of the applciation. The purpose of the web app
is to change the status of the Applications, for which all actions have been provided.


Link to deployed version of app: https://recruitment-app-hackertrail.herokuapp.com/
