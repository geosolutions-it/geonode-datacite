# django-datacite

Let Geonode generate DataCites DOI using custom metadata integrated in Geonode

### How to configure it

```

INSTALLED_APPS += ('geonode_datacite',)
DATACITE_API_URL="https://api.test.datacite.org"
DATACITE_API_USERNAME=""
DATACITE_API_PASSWORD=""
DATACITE_PREFIX="10.82863"
DATACITE_CREATOR=""
DATACITE_CREATOR_TYPE="Organizational"
DATACITE_PUBLISHER="CNR"

```

### Metadata required for datacite publishing

Follows the payload send to datacite

```json
{
            "data": {
                "type": "dois",
                "attributes": {
                    "event": data.get("event", "draft"),
                    "prefix": data.get("prefix", self.prefix),
                    "creators": [
                        {
                            "name": data.get("creator", settings.DATACITE_CREATOR),
                            "nameType": data.get(
                                "creator_type", settings.DATACITE_CREATOR_TYPE
                            ),
                        }
                    ],
                    "titles": [
                        {
                            "lang": data.get("lang", get_language()),
                            "title": data.get("title"),
                        }
                    ],
                    "publisher": {
                        "lang": data.get("lang", get_language()),
                        "publisher": data.get(
                            "publisher", settings.DATACITE_PUBLISHER
                        ),
                    },
                    "publicationYear": data.get(
                        "publication_year", datetime.now().strftime("%Y")
                    ),
                    "types": {
                        "resourceTypeGeneral": data.get(
                            "resource_type", "Other"
                        ).title()
                    },
                    "url": data.get("url"),
                },
            }
        }
```

In detail:

- **`event`**: is the action to be performed on datacite `draft` or `findable`, is decided base on the button clicked in the UI
- **`prefix`**: if not passed, is automatically retrieved (default behaviour) from the setting *DATACITE_PREFIX* 
- **`creator - name`**: if not passed is automatically retrieved (default behaviour) from the setting *DATACITE_CREATOR*
- **`creator - nameType`**: if not passed is automatically retrieved (default behaviour) from the setting *DATACITE_CREATOR_TYPE*
- **`titles - lang`**: it use the value *language* of the resource, if is not defined the language is retrieved via the django helper function [get_language()](https://github.com/django/django/blob/35c58a7924aa07e87e925f6eea978c278f143f36/django/utils/translation/trans_real.py#L326-L335)
- **`titles - title`**: it use the title of the dataset
- **`publisher - lang`**: it use the value *language* of the resource, if is not defined the language is retrieved via the django helper function [get_language()](https://github.com/django/django/blob/35c58a7924aa07e87e925f6eea978c278f143f36/django/utils/translation/trans_real.py#L326-L335)
- **`publisher - publisher`**: if not passed is automatically retrieved (default behaviour) from the setting *DATACITE_PUBLISHER*
- **`publicationYear`**: if not passed, it uses the current year
- **`types - resourceTypeGeneral`**: converts automatically the default dataset subtype into a Datacite known list. The list is available in the *utils.py* file (`DATACITE_TYPE_MAPPING`)
- **`url`**: it generates an url using the UUID of the dataset

The above payload can be extended as needed. The above one is the minimun payload required to publish on DataCite. The mapping and its definition can be found in the official [DataCite documentation](https://support.datacite.org/docs/api-create-dois)

#### For developers:

The payload is generated in the admin.py file when datacite_handler.create_doi() is called. The handler will automatically generates the payload required for DataCite, so any additional payload must be added there.
The payload on the handler side, is availabe in the DataCiteHandler.generate_schema() method. Is a normal python dict and can be extended as needed