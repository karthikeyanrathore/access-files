from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):

    # Note: id is automatically created.
    # https://docs.djangoproject.com/en/5.0/topics/db/models/#quick-example
    CLASS_TYPES = (
        ("ITD", "IT documents"),
        ("SD", "Staff documents"),
        ("ED", "Exam documents"),
        ("STD", "Student documents"),
        # docs from received from other schools/companies/organizations.
        ("EXD", "External documents"),
        ("MD", "Marketing documents")
    )

    project_name = models.CharField(max_length=40, null=False, blank=False, unique=True)
    project_class = models.CharField(choices=CLASS_TYPES, max_length=30)
    description = models.CharField(max_length=250, null=True, blank=True)
    users = models.ManyToManyField(User, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Note: files will be defined in File model as foreign key.

    def __str__(self):
        return f"{self.id}: {self.project_name} / {self.project_class}"



class File(models.Model):

    filename = models.CharField(max_length=40, null=False, blank=False, unique=True)
    # one to many relation
    author =  models.ForeignKey(User, related_name="files", on_delete=models.CASCADE)
    file_bytes = models.BinaryField(null=False, blank=False)
    # one to many relation
    project = models.ForeignKey(Project, related_name="files", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.filename}"





# 
# python manage.py makemigrations file_system
# python manage.py migrate --run-syncdb
