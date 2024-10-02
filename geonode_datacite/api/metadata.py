class DataCiteMetadataHandler:
    """
    DataCite requires additional metadata information which are not included by default
    in GeoNode
    """

    def get_fields(self):
        """
        Required fields for DataCiete schema:
            - DOI
            - State
            - URL
            - Creators (maybe resource owner or admin?)
            - Title
            - Title type (enum (Alternative, Subtitle, TranslatedTitle, Other))
            - Resource Language with the entity that hold/produce the resource (see DataCiteFrabrica for the list)
            - Publication Year (maybe the year when the resource is created?)
            - ResourceTypeGeneral: enum of the general type of the resource (see DataCiteFrabrica for the list)
        """
        pass
