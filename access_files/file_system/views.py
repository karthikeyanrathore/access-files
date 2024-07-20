from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

from file_system.models import Project

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

class HealthCheckView(views.APIView):

    def get(self, request):
        message = "Ok - server response."
        return Response(
            data={"message": message},
            status=status.HTTP_200_OK
        )


class ProjectsView(views.APIView):
    # https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []
        projects = Project.objects.all()
        for project in projects:
            data.append(project.serialize())
        return Response(
            data={"message": data},
            status=status.HTTP_200_OK
        )

    # Note: only superuser can use this endpoint to create
    # project.
    def post(self, request):
        token = request.headers["Authorization"][7:]
        access_token = (AccessToken(token))
        user_id = (access_token.get("user_id"))
        user = User.objects.get(id=user_id)
        
        if not user.is_superuser:
            print("Ok - invalid superuser.")
            message = "Only superuser can created projects."
            return Response(
                data={"error": message},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        payload = self.request.data
        if "project_class" not in payload.keys() or "project_name" not in payload.keys():
            message = "missing data in payload."
            return Response(
                data={"error": message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # try:
        #     is_project = Project.objects.get(project_name=payload.get("project_name"))
        # except ObjectDoesNotExist:
        #     message = ""
        default_descr = "default project"
        description = payload.get("description") if payload.get("description") else default_descr
        try:
            project = Project(
                project_name=payload.get("project_name"),
                project_class=payload.get("project_class"),
                description=description,
            )
            project.full_clean()
            project.save()
        except IntegrityError as error:
            message = f"Ok - project name already exists."
            return Response(
                data={"error": message},
                status=status.HTTP_403_FORBIDDEN,
            )
        except ValidationError as error:
            message = f"Validation error: {error}"
            return Response(
                data={"error": message},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = project.serialize()
        return Response(
            data={"message": data},
            status=status.HTTP_200_OK
        )


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