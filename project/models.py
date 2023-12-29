from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from guardian.shortcuts import assign_perm
import re


def directoryPath_old(instance, filename):
    # file will be uploaded to MEDIA_ROOT/id-<id>/<filename>
    cleanString = re.sub('\W+', '', instance.project.name)
    # TODO: Colocar o Nome/Id de usuario
    print('id-{0}/proj-{1}/{2}'.format(instance.id, cleanString, filename))
    return 'id-{0}/proj-{1}/{2}'.format(instance.id, cleanString, filename)


class Project(models.Model):

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("project:project_detail", args=[self.slug])

    class Meta:
        permissions = [
            ("can_add_new_project", "can add new project"),
            ("dg_view_project", "OLP can view project"),
        ]

    def __str__(self):
        return self.name


@receiver(post_save, sender=Project)
def set_permission(sender, instance, **kwargs):
    assign_perm("dg_view_project", instance.user, instance)


class Image(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=directoryPath_old)
