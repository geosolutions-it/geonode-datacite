from django.test import SimpleTestCase, TestCase

from geonode_datacite.api.handler import DataCiteHandler

# Create your tests here.


class TestDataciteSchema(SimpleTestCase):
    def setUp(self) -> None:
        self.sut = DataCiteHandler()
        self.context = {
            "prefix": "10.82433",
            "creators": [{"name": "GeoSolutions", "nameType": "Organizational"}],
            "titles": [{"lang": "en", "title": "Example title"}],
            "publisher": {"lang": "en", "name": "GeoSolutions"},
            "publication_year": 2024,
            "url": "https://geosolutionsgroup.com",
        }

    def test_creation_of_datacite_schema(self):
        result = self.sut.generate_schema(context=self.context, as_json=False)
        self.assertTrue(isinstance(result, str))

        result = self.sut.generate_schema(context=self.context, as_json=True)
        self.assertTrue(isinstance(result, dict))

    def test_create_doi(self):
        response = self.sut.create_doi(data=self.context)
        self.assertTrue(200, response.status_code)

    def test_update_doi(self):
        context = {
            "data": {
                "type": "dois",
                "attributes": {
                    "types": {"resourceTypeGeneral": "Dataset"},
                    "doi": "10.82863/pvsq-2183",
                },
            }
        }
        response = self.sut.update_doi(data=context)
        self.assertTrue(200, response.status_code)
