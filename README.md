# django-datacite

Let Geonode generate DataCites DOI using custom metadata integrated in Geonode

### How to configure it

```

INSTALLED_APPS += ('geonode_datacite',)
DATACITE_API_URL="https://api.test.datacite.org"
DATACITE_API_USERNAME="ZJTW.WYGJIS"
DATACITE_API_PASSWORD="nEcgih-1fespu-wesrib"
DATACITE_EVENT='findable'
DATACITE_EVENT="10.82863"
DATACITE_CREATOR="CNR"
DATACITE_CREATOR_TYPE="Organizational"
DATACITE_PUBLISHER="CNR"

```