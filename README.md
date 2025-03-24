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
