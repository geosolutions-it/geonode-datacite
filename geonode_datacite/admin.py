import logging
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path

from geonode_datacite.handler import datacite_handler
from geonode_datacite.models import DataCite
from geonode.base.models import ResourceBase
from django.urls import reverse
from django.contrib import messages
from geonode.utils import build_absolute_uri

logger = logging.getLogger(__name__)
# Register your models here.


class DataCiteAdmin(admin.ModelAdmin):
    model = ResourceBase
    #list_display = ('resource', 'url', 'created_at', 'updated_at')
    change_list_template = "admin/client/change_list.html"

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ("resource", 'url', 'created_at', "updated_at")
        return self.readonly_fields

    def get_queryset(self, request):
        if '/change' in request.path:
            return DataCite.objects.filter(pk=request.resolver_match.kwargs['object_id'])
        return ResourceBase.objects.filter(is_published=True, is_approved=True)
    
    def get_urls(self):
        return [
            path("generate/<resource_pk>", self.admin_site.admin_view(self.generate_doi), name="generate-doi"),
        ] + super().get_urls()

    def generate_doi(self, request, resource_pk):
        # getting GeoNode Resource
        try:
            resource = get_object_or_404(ResourceBase, pk=resource_pk)
            # callid datacite for the DOI generation
            response = datacite_handler.create_doi(
                data={
                    "title": resource.title,
                    "language": resource.language,
                    "resource_type": settings.DATACITE_TYPE_MAPPING.get(resource.subtype),
                    "url": build_absolute_uri(resource.detail_url)
                }
            )
            data = response.json()
            obj = DataCite(
                resource=resource,
                url=f"{settings.DATACITE_DETAIL_URL}/{data['data']['id']}"
            )
            obj.save()
            ResourceBase.objects.filter(pk=resource_pk).update(doi=data['data']['id'])
            messages.add_message(request, messages.SUCCESS, f'DOI has been published for resource {resource.title}')
        except Exception as e:
            logger.exception(e)
            messages.add_message(request, messages.ERROR, f'Some error has occured while publishing the DOI {e}')
        return HttpResponseRedirect(reverse("admin:geonode_datacite_datacite_changelist"))

admin.site.register(DataCite, DataCiteAdmin)
