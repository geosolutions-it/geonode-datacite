import os

project_dir = os.path.dirname(os.path.abspath(__file__))

VERSION = (0, 0, 1)
__version__ = ".".join([str(i) for i in VERSION])
__author__ = "geosolutions-it"
__email__ = "info@geosolutionsgroup.com"
__url__ = "https://github.com/geosolutions-it/geonode-datacite"
default_app_config = "geonode_datacite.apps.GeonodeDataciteConfig"
