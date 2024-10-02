from django.apps import AppConfig
from geonode.metadata.registry import metadata_registry


class GeonodeDataciteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geonode_datacite"

    def ready(self):
        metadata_registry.register_new_app(
            "geonode_datacite.api.metadata.DataCiteMetadataHandler"
        )
