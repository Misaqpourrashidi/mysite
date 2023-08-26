from django.contrib import admin
from shop.models import (
	Customer,
	OrderProduct,
	Order,
	Address,
	Payment
)

class OrderAdmin(admin.ModelAdmin):
	list_display = [
		'user',
		'ordered',
		'sent',
		'received',
		'address',
	]

	list_filter = [
		'ordered',
		'sent',
		'received',
	]
	list_display_links = [
	'user',
	]
	search_fields = [
		'user__user__phone_number',
		'ref_code',
	]

admin.site.register(Customer)
admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
admin.site.register(Payment)