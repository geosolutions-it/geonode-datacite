from django.apps import AppConfig


class GeonodeDataciteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geonode_datacite"
    verbose_name = "GeoNode DataCite"

    def ready(*args, **kwargs):

        # from geonode.api.urls import router
        import os
        from django.conf import settings
        from geonode.security.registry import permissions_registry

        LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

        settings.TEMPLATES[0]["DIRS"].insert(0, os.path.join(LOCAL_ROOT, "templates"))

        permissions_registry.add(
            "geonode_datacite.permissions.DataCitePermissionsHandler"
        )
