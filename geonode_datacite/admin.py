import logging
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import path

from geonode_datacite.forms import DataCiteForm
from geonode_datacite.utils import DATACITE_TYPE_MAPPING
from geonode_datacite.handler import datacite_handler
from geonode_datacite.models import DataCite
from geonode.base.models import ResourceBase
from geonode.documents.models import Document
from django.urls import reverse
from django.contrib import messages
from geonode.utils import build_absolute_uri
from geonode.resource.manager import resource_manager

logger = logging.getLogger(__name__)
# Register your models here.


class DataCiteAdmin(admin.ModelAdmin):
    model = ResourceBase
    form = DataCiteForm
    change_list_template = "admin/client/change_list.html"

    def get_readonly_fields(self, request, obj=None):
        """
        Return the readonly fields for the change. view of the datacite.
        Once is created, it cannot be updated
        """
        if obj:  # editing an existing object
            return self.readonly_fields + (
                "resource",
                "url",
                "created_at",
                "updated_at",
            )
        return self.readonly_fields
    
    def get_queryset(self, request):
        """
        Customize the queryset based on the call. For the change, we will return the datacite
        for the listing, we will return resourcebase
        for the deleting, we can return all the datacite, django will sort them after
        """
        # TODO improve me, find a better way to show the resource listing
        if "/change" in request.path:
            # if is a change, we need to return the datacite object
            return DataCite.objects.filter(
                pk=request.resolver_match.kwargs["object_id"]
            )
        if request.POST.get("action", "") == 'delete_selected':
            # if is a post, means we want to delete the object so we have to return the 
            # datacite object
            return DataCite.objects.all()
        return ResourceBase.objects.filter(is_published=True, is_approved=True)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        We will return only the resources without any datacite associated
        """
        if db_field.name == "resource":
            kwargs["queryset"] = ResourceBase.objects.filter(is_published=True, is_approved=True, datacite__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_urls(self):
        """
        Add custom urls for manage the datacite operations
        """
        return [
            path(
                "findable/<resource_pk>/confirmation",
                self.admin_site.admin_view(self.confirmation),
                name="confirmation-doi",
            ),
            path(
                "findable/<resource_pk>",
                self.admin_site.admin_view(self.findable),
                name="confirmation-doi",
            ),
            path(
                "draft/<resource_pk>",
                self.admin_site.admin_view(self.draft),
                name="draft-doi",
            ),
        ] + super().get_urls()

    def confirmation(self, request, resource_pk):
        """
        Confirmation page, is called before a user try to publish to datacite in 
        findable state
        """
        if request.method == "POST":
            return self.findable(request, resource_pk)
        resource = get_object_or_404(ResourceBase, pk=resource_pk)
        return render(request, "admin/client/confirmation.html", {"resource": resource})
    
    def draft(self, request, resource_pk):
        return self.generate_doi(request, resource_pk, event=DataCite.State.draft)

    def findable(self, request, resource_pk):
        return self.generate_doi(request, resource_pk, event=DataCite.State.findable)

    def generate_doi(self, request, resource_pk, event):
        """
        Creates the DOI in Datacite and then update the DOI in GeoNode
        """
        # getting GeoNode Resource
        try:
            resource = get_object_or_404(
                ResourceBase, pk=resource_pk
            ).get_real_instance()
            resource_type = resource.subtype
            if isinstance(resource, Document):
                resource_type = resource.extension

            # callid datacite for the DOI generation

            response = datacite_handler.create_doi(
               data={
                   "event": event,
                   "title": resource.title,
                   "language": resource.language,
                   "resource_type": DATACITE_TYPE_MAPPING.get(resource_type),
                   "url": build_absolute_uri(resource.detail_url)
               }
            )
            data = response.json()

            obj = DataCite(
                resource=resource,
                url=f"{settings.DATACITE_DETAIL_URL}/{data['data']['id']}",
                state=event,
            )
            obj.save()
            # update resource object
            resource_manager.update(
                str(resource.uuid), resource=resource, vals={"doi": data["data"]["id"]}
            )

            messages.add_message(
                request,
                messages.SUCCESS,
                f"DOI has been published for resource: {resource.title}",
            )
        except Exception as e:
            logger.error(e)
            messages.add_message(
                request,
                messages.ERROR,
                f"Some error has occured while publishing the DOI: {e}",
            )
        return HttpResponseRedirect(
            reverse("admin:geonode_datacite_datacite_changelist")
        )


admin.site.register(DataCite, DataCiteAdmin)
