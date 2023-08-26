from django.contrib import admin

from product.models import Product, Category, SubCategory, Images


class ProductAdmin(admin.ModelAdmin):
	list_display = [
		'product_title',
		'slug',
	]


admin.site.register(Product, ProductAdmin)	
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Images)