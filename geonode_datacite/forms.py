from django import forms

from geonode_datacite.models import DataCite
from geonode_datacite.utils import update_resource_doi



class DataCiteForm(forms.ModelForm):

    doi = forms.CharField(required=False)
    class Meta:
        model = DataCite
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.fields, "doi"):
            self.fields['doi'].initial = self.instance.resource.doi

    def save(self, commit = ...):
        instance = super().save(commit)
        
        # updating DOI with the one provided vua form
        update_resource_doi(instance.resource, self.cleaned_data['doi'])

        return instance