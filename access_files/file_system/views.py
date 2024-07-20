from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

from file_system.models import Project, File

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser, MultiPartParser



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
    permission_classes = [IsAuthenticated]

    # Note: only superuser can assign a user to a project.
    def post(self, request, project_id):
        token = request.headers["Authorization"][7:]
        access_token = (AccessToken(token))
        atoken_user_id = (access_token.get("user_id"))
        atoken_user = User.objects.get(id=atoken_user_id)
        
        if not atoken_user.is_superuser:
            print("Ok - invalid superuser.")
            message = "Only superuser can created projects."
            return Response(
                data={"error": message},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        payload = self.request.data
        if "user_id" not in payload.keys():
            message = "missing user_id in payload"
            return Response(
                data={"error": message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            project = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            message = "Ok - project does not exists."
            return Response(
                data={"error": message},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            assigned_user = User.objects.get(id=int(payload.get("user_id")))
        except ObjectDoesNotExist:
            message = "Ok - user does not exists."
            return Response(
                data={"error": message},
                status=status.HTTP_404_NOT_FOUND,
            )
        # print(assigned_user)
        # TODO: check if user is already assigned or not.

        project.users.add(assigned_user)
        project.save()
        # data = project.serialize()
        print(f"Ok - Assigned user_id: {assigned_user.id} to project_id: {project_id}")
        return Response(
            data={"message": "Ok - Assigned user to project."},
            status=status.HTTP_200_OK
        )
        

class PublishFilesView(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    # Note: only superuser or user with right access to project
    # can publish files to project.
    # check for any malware in file before savin it in db.
    def post(self, request, project_id):
        token = request.headers["Authorization"][7:]
        access_token = (AccessToken(token))
        atoken_user_id = (access_token.get("user_id"))
        atoken_user = User.objects.get(id=atoken_user_id)

        ## (self.request.data)
        try:
            project = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            message = "Ok - project does not exists."
            return Response(
                data={"error": message},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            project = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            message = "Ok - project does not exists."
            return Response(
                data={"error": message},
                status=status.HTTP_404_NOT_FOUND,
            )
        assigned_users = [int(user.id) for user in project.users.all()]
        if atoken_user.is_superuser or (atoken_user_id in assigned_users):
            # publish file
            files = request.FILES
            # print(files["file"].read())
            # TODO encrypt file bytes fernet.
            try:
                for k in files.keys():
                    fbytes = files[k].read()
                    assert isinstance(fbytes, bytes) == True
                    f = File(
                        author=atoken_user,
                        file_bytes=fbytes,
                        filename=files[k],
                        project=project,
                    )
                    f.save()
            except IntegrityError:
                message  = "filename already exists."
                return Response(
                    data={"error": message},
                    status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                data={"message": "Ok - published file."},
                status=status.HTTP_200_OK
            )
        return Response(
            data={"message": "Invalid user - User does not have permission to publish files to project."},
            status=status.HTTP_403_FORBIDDEN
        )


class ProjectFilesView(views.APIView):
    permission_classes = [IsAuthenticated]

    # Note: user with right access to project can 
    # view all the files in that project.
    def get(self, request, project_id):
        token = request.headers["Authorization"][7:]
        access_token = (AccessToken(token))
        atoken_user_id = (access_token.get("user_id"))
        atoken_user = User.objects.get(id=atoken_user_id)

        try:
            project = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            message = "Ok - project does not exists."
            return Response(
                data={"error": message},
                status=status.HTTP_404_NOT_FOUND,
            )
        if atoken_user.is_superuser:
            return Response(
                data={"message": "OK"},
                status=status.HTTP_200_OK
            )
        ret = {}
        fo = []
        files = (project.files.all())
        for file in files:
            fo.append({"id": file.id, "filename": file.filename, "author": file.author.username})
        ret["project_class"] = project.project_class
        ret["project_name"] = project.project_name
        ret["files"] = fo
        assigned_users = [int(user.id) for user in project.users.all()]
        # print(assigned_users)
        # print(atoken_user_id)
        if atoken_user_id in assigned_users:
            return Response(
                data={"message": ret},
                status=status.HTTP_200_OK
            )
        return Response(
            data={"message": f"user_id: {atoken_user_id} does not belong to the project."},
            status=status.HTTP_200_OK
        )



class DownloadFileView(views.APIView):
    pass