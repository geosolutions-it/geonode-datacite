import base64
from datetime import datetime
import requests
import logging

from typing import Dict
from django.conf import settings
from django.utils.translation import get_language

logger = logging.getLogger("geonode")


class DataCiteHandler:
    """
    GeoNode DataCiteHandler, object to validate the geonode metadata
    for generate DataCite DOI
    https://support.datacite.org/docs/api
    """

    def __init__(self) -> None:
        self.url = settings.DATACITE_API_URL
        self.user = settings.DATACITE_API_USERNAME
        self.password = settings.DATACITE_API_PASSWORD
        self.prefix = getattr(settings, "DATACITE_PREFIX", "10.82863")

    def create_doi(self, data: Dict = {}) -> Dict:
        """
        Given the context will populate the DataCite doi metadata schema
        to generate the DOI via API
        """
        context = self.generate_schema(data=data)
        return self.call_api(context, method="POST")

    def update_doi(self, data: Dict = {}, pk: str = None) -> Dict:
        """
        Given the context will update a DOI via API
        """
        data = self.generate_schema(data=data)
        return self.call_api(data, method="PATCH", pk=pk)

    def search_doi(self, pk: str = None) -> Dict:
        """
        Given the Doi IS will search it via API
        """
        return self.call_api({}, method="GET", pk=pk)

    def delete_doi(self, pk: str = None) -> Dict:
        """
        Given the context will delete the DOI. Must be in draft state
        DOIs in Registered or Findable state cannot be deleted
        https://support.datacite.org/docs/can-i-delete-or-change-my-dois
        """
        return self.call_api({}, method="DELETE", pk=pk)

    def call_api(self, data: Dict, method: str, pk: str = "") -> Dict:
        """
        create the DOI via API and return the payload generated
        """

        access = f"{self.user}:{self.password}".encode()
        headers = {
            "accept": "application/vnd.api+json",
            "content-type": "application/json",
            "authorization": f"Basic {base64.b64encode(access).decode()}",
        }
        url = f"{self.url}/dois/" + pk
        response = None
        try:
            http_metod = getattr(requests, method.lower())
            response = http_metod(
                url,
                json=data,
                headers=headers,
            )
            response.raise_for_status()
        except Exception as e:
            if response is not None:
                logger.error(response.json())
            raise e
        return response

    def generate_schema(self, data: Dict = {}) -> Dict:
        """
        Given the context will populate the DataCite doi metadata schema
        to generate the DOI via API
        """
        return {
            "data": {
                "type": "dois",
                "attributes": {
                    "event": data.get("event", "draft"),
                    "prefix": data.get("prefix", self.prefix),
                    "creators": data.get("creators", []),
                    "titles": [
                        {
                            "lang": data.get("lang", get_language()),
                            "title": data.get("title"),
                        }
                    ],
                    "publisher": data.get("publisher", {}),
                    "publicationYear": data.get(
                        "publication_year", datetime.now().strftime("%Y")
                    ),
                    "types": {
                        "resourceTypeGeneral": data.get(
                            "resource_type", "Other"
                        ).title()
                    },
                    "identifiers": [
                        {
                            "identifier": data.get("uuid"),
                            "identifierType": "UUID",
                        }
                    ],
                    "url": data.get("url"),
                    "language": settings.DATACITE_LANGUAGE,
                    "rightsList": [{
                            "rights": data.get("license_name"),
                            }],
                    "descriptions": data.get("descriptions", []),
                    "geoLocations": data.get("geolocations", []),
                    "sizes": data.get("sizes", []),
                    "formats": data.get("format", []),
                    
                },
            }
        }


datacite_handler = DataCiteHandler()
