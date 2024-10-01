import base64
import json
import requests
import logging

from typing import Dict
from django.conf import settings
from django.template.loader import get_template

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

    def call_api(self, data: Dict, method: str, pk: str= None) -> Dict:
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

    def create_doi(self, data: Dict = {}) -> Dict:
        """
        Given the context will populate the DataCite doi metadata schema
        to generate the DOI via API
        """
        context = self.generate_schema(context=data)
        return self.call_api(context, method="POST")

    def update_doi(self, data: Dict = {}, pk: str = None) -> Dict:
        """
        Given the context will update a DOI via API
        """
        return self.call_api(data, method="PATCH", pk=pk)

    def generate_schema(
        self, context: Dict = {}, template: str = "create_doi.json", as_json=True
    ) -> Dict:
        """
        Given the context will populate the DataCite doi metadata schema
        to generate the DOI via API
        """
        context["prefix"] = self.prefix
        t = get_template(template)
        t_as_str = t.render(context=context)
        return t_as_str if not as_json else json.loads(t_as_str.replace("'", '"'))
