from django.apps import AppConfig

class GeonodeDataciteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geonode_datacite"
    verbose_name = "GeoNode DataCite"

    def run_setup_hooks(*args, **kwargs):

        # from geonode.api.urls import router
        import os
        from django.conf import settings

        LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

        settings.TEMPLATES[0]["DIRS"].insert(0, os.path.join(LOCAL_ROOT, "templates"))
