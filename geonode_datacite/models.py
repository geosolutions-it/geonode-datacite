from django.db import models
from geonode.base.models import ResourceBase


class DataCite(models.Model):
    """
    Basic model to store datacite DOI urls 
    """

    resource = models.ForeignKey(ResourceBase, on_delete=models.SET_NULL, null=True)
    url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.resource.title

    class Meta:
        verbose_name_plural = "Data Cite"
