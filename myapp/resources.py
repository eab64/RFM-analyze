from import_export import resources
from .models import Information, Additional

class InformationResource(resources.ModelResource):
    class Meta:
        model = Information

class AdditionalResource(resources.ModelResource):
    class Meta:
        model = Additional
