from django.contrib import admin
from file_system.models import Project, File


# Register your models here.

class FileSystemAdmin(admin.ModelAdmin):
    list_display = ("filename", "author", "project")


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ("project_name", "project_class", "total_files")

    def total_files(self, x):
        return x.files.count()


admin.site.register(Project, ProjectsAdmin)
admin.site.register(File, FileSystemAdmin)

