from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from w_date.models import (
	Day, 
	Month_Name, 
	Year,
	January, 
	February,
	March,
	April,
	May,
	June,
	July,
	August,
	September,
	October,
	November,
	December,
)

class DayAdmin(ImportExportModelAdmin):
	...

class JanuaryAdmin(ImportExportModelAdmin):
	...


admin.site.register(Day, DayAdmin)
admin.site.register(Month_Name)
admin.site.register(Year)
admin.site.register(January, JanuaryAdmin)
admin.site.register(February)
admin.site.register(March)
admin.site.register(April)
admin.site.register(May)
admin.site.register(June)
admin.site.register(July)
admin.site.register(August)
admin.site.register(September)
admin.site.register(October)
admin.site.register(November)
admin.site.register(December)
