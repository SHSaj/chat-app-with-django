from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Friend



class AccountAdmin(UserAdmin):
	list_display = ('email','username','is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('id',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register([Friend])