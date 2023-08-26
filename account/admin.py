from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, State, City
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group



class AccountAdmin(UserAdmin):
	list_display = ('phone_number','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username')
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

class StateAdmin(ImportExportModelAdmin):
	...

class CityAdmin(ImportExportModelAdmin):
	...

admin.site.register(Account, AccountAdmin)	
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)


admin.site.unregister(Group)

admin.site.site_header = "MY WEBSITE"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcom To Admin Panel"