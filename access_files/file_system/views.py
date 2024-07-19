from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, views


class HealthCheckView(views.APIView):

    def get(self, request):
        message = "Ok, server response."
        return Response(
            data={"message": message},
            status=status.HTTP_200_OK
        )


class ProjectsView(views.APIView):
    
    def get(self, request):
        pass

    # Note: only superuser can use this endpoint to create
    # project.
    def post(self, request):
        pass


class AssignProjectView(views.APIView):
    
    # Note: only superuser can assign a user to a project.
    def post(self, request, project_id, user_id):
        pass



class PublishFilesView(views.APIView):

    # Note: only superuser or user with right access to project
    # can publish files to project.
    # check for any malware in file before savin it in db.
    def post(self, request, project_id):
        pass



class ProjectFilesView(views.APIView):

    # Note: user with right access to project can 
    # view all the files in that project.
    def get(self, request, project_id):
        pass