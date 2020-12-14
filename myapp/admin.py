from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Information, Additional


@admin.register(Information)

class InformationAdmin(ImportExportModelAdmin):
    list_display = ('Name', 'Number', 'Income', 'Visit_count',
                    )

@admin.register(Additional)

class AdditionalAdmin(ImportExportModelAdmin):
    list_display = ('Number', 'Visit_data', 'Visit_status',
                    )


