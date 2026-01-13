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
from geonode.metadata.manager import metadata_manager

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
            resource_type = settings.DATACITE_RESOURCE_TYPE_GENERAL
            # Extract geolocations from bbox
            geolocations = []
            if resource.bbox:
                try:
                    bbox = resource.bbox
                    xmin, xmax, ymin, ymax = bbox[0], bbox[1], bbox[2], bbox[3]
                    
                    # Calculate center point
                    center_lon = (xmin + xmax) / 2
                    center_lat = (ymin + ymax) / 2
                    
                    geolocation = {
                        "geoLocationPoint": {
                            "pointLongitude": center_lon,
                            "pointLatitude": center_lat
                        },
                        "geoLocationBox": {
                            "westBoundLongitude": xmin,
                            "eastBoundLongitude": xmax,
                            "southBoundLatitude": ymin,
                            "northBoundLatitude": ymax
                        }
                    }
                    geolocations.append(geolocation)
                except Exception as e:
                    print("Error extracting geolocation:", e)

            try:
                metadata = metadata_manager.build_schema_instance(resource)
            except Exception as e:
                logger.warning(f"Could not extract metadata using metadata_manager: {e}")
                metadata = {}
            # Extract creators from metadata (cnr_creator)
            creators = []
            cnr_creators = metadata.get('cnr_creator', [])
            if isinstance(cnr_creators, list):
                for cnr_c in cnr_creators:
                    fullname = cnr_c.get('fullname', '').strip()
                    orcid = cnr_c.get('orcid')
                    if not fullname and not orcid:
                        continue
                    
                    creator = {
                        "nameType": "Personal",
                    }
                    
                    if fullname:
                        name_parts = fullname.rsplit(' ', 1)
                        if len(name_parts) == 2:
                            creator["givenName"] = name_parts[0]
                            creator["familyName"] = name_parts[1]
                    
                    if orcid:
                        creator["nameIdentifiers"] = [{
                            "nameIdentifier": orcid,
                            "schemeUri": "https://orcid.org",
                            "nameIdentifierScheme": "ORCID"
                        }]
                    
                    creators.append(creator)


            # Publisher with ROR identifier
            publisher = {
                "name": settings.DATACITE_PUBLISHER,
                "publisherIdentifier": settings.DATACITE_PUBLISHER_ROR_ID,
            }

            try:
                link = resource.link_set.filter(link_type='data').last()
                format = [link.mime] if link and link.mime else []
            except Exception:
                format = []
            
            # Descriptions from abstract
            descriptions = []
            if resource.abstract:
                descriptions.append({
                    "description": resource.abstract,
                    "descriptionType": "Abstract"
                })

            # Size from metadata (cnr_file_size)
            sizes = []
            file_size = metadata.get('cnr_file_size')
            if file_size:
                sizes.append(str(file_size))

            # callid datacite for the DOI generation

            response = datacite_handler.create_doi(
               data={
                   "event": event,
                   "title": resource.title,
                   "language": resource.language,
                   "resource_type": resource_type,
                   "url": build_absolute_uri(reverse("resolve_uuid", args=[resource.uuid])),
                   "abstract": resource.abstract,
                   "uuid": resource.uuid,
                   "license_name": str(resource.license) if resource.license else '',
                   "geolocations": geolocations,
                   "creators": creators,
                   "publisher": publisher,
                   "descriptions": descriptions,
                   "sizes": sizes,
                   "format": format,
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
