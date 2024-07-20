from django.db import models
from django.contrib.auth.models import User
from access_files.settings import CLASS_TYPES

class Project(models.Model):

    project_name = models.CharField(max_length=40, null=False, blank=False, unique=True)
    project_class = models.CharField(choices=CLASS_TYPES, max_length=30)
    description = models.CharField(max_length=250, null=True, blank=True)
    users = models.ManyToManyField(User, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Note: files will be defined in File model as foreign key.

    def __str__(self):
        return f"{self.id}: {self.project_name} / {self.project_class}"
    
    def serialize(self):
        out = {}
        out["id"] = self.id
        out["project_name"] = self.project_name
        out["project_class"] = self.project_class
        out["description"] = self.description
        out["created_at"] = self.created_at
        out["updated_at"] = self.updated_at
        staff = []
        for user in self.users.all():
            staff.append({
                "user_id": user.id, 
                "username": user.username,
                "is_superuser": user.is_superuser,
            })        
        out["users"] = staff
        return out


class File(models.Model):

    filename = models.CharField(max_length=40, null=False, blank=False, unique=True)
    # one to many relation
    author =  models.ForeignKey(User, related_name="files", on_delete=models.CASCADE)
    file_bytes = models.BinaryField(null=False, blank=False)
    # one to many relation
    project = models.ForeignKey(Project, related_name="files", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.filename}"

    def serialize(self):
        pass


# class FileAccessLog():
#     pass


# docker-compose up
# python manage.py makemigrations file_system
# python manage.py migrate --run-syncdb
# python manage.py createsuperuser --username admin --email admin@school.com