# django-datacite

Let Geonode generate DataCites DOI using custom metadata integrated in Geonode

### How to configure it

```

INSTALLED_APPS += ('geonode_datacite',)
DATACITE_API_URL="https://api.test.datacite.org"
DATACITE_API_USERNAME=""
DATACITE_API_PASSWORD=""
DATACITE_EVENT='findable'
DATACITE_EVENT="10.82863"
DATACITE_CREATOR=""
DATACITE_CREATOR_TYPE="Organizational"
DATACITE_PUBLISHER=""
DATACITE_TYPE_MAPPING = {
    "txt": "Text",
    "csv": "Text",
    "log": "Text",
    "doc": "Text",
    "docx": "Text",
    "ods": "Text",
    "odt": "Text",
    "sld": "Text",
    "qml": "Text",
    "xls": "Text",
    "xlsx": "Text",
    "xml": "Text",
    "bm": "Image",
    "bmp": "Image",
    "dwg": "Image",
    "dxf": "Image",
    "fif": "Image",
    "gif": "Image",
    "jpg": "Image",
    "jpe": "Image",
    "jpeg": "Image",
    "png": "Image",
    "tif": "Image",
    "tiff": "Image",
    "pbm": "Report",
    "odp": "Report",
    "ppt": "Report",
    "pptx": "Report",
    "pdf": "Report",
    "tar": "PhysicalObject",
    "tgz": "PhysicalObject",
    "rar": "PhysicalObject",
    "gz": "PhysicalObject",
    "7z": "PhysicalObject",
    "zip": "PhysicalObject",
    "aif": "Sound",
    "aifc": "Sound",
    "aiff": "Sound",
    "au": "Sound",
    "mp3": "Sound",
    "mpga": "Audiovisual",
    "wav": "Audiovisual",
    "afl": "Audiovisual",
    "avi": "Audiovisual",
    "avs": "Audiovisual",
    "fli": "Audiovisual",
    "mp2": "Sound",
    "mp4": "Audiovisual",
    "mpg": "Audiovisual",
    "ogg": "Audiovisual",
    "webm": "Audiovisual",
    "3gp": "Audiovisual",
    "flv": "Audiovisual",
    "vdo": "Other",
    "glb": "Other",
    "pcd": "Other",
    "gltf": "Other",
    "ifc": "Other",
    "vector": "Dataset",
    "dataset": "Dataset",
    "vector_time": "Dataset",
    "raster": "Dataset"
}
```
