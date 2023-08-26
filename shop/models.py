from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, date
from django.core.validators import MinLengthValidator
from product.models import Product


class Customer(models.Model):
	user 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	session_key 			= models.CharField(max_length=200, blank=True)

	def __str__(self):
		return f'{self.user}  {self.session_key}'




class OrderProduct(models.Model):
	user 					= models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
	ordered 				= models.BooleanField(default=False)
	item 					= models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity				= models.IntegerField(default=1, blank=True)

	def __str__(self):
		return f'{self.user} | {self.quantity} of {self.item.product_title}'


	def get_total_item_price(self):
		return self.item.price * self.quantity


	def get_total_discount_price(self):
		if self.item.discount_price:
			return self.item.discount_price * self.quantity
		return 0

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_total_discount_price()

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_amount_saved()
		return self.get_total_item_price()


class Order(models.Model):
	user 					= models.ForeignKey(Customer, on_delete=models.CASCADE)
	ref_code 				= models.CharField(max_length=20, blank=True)
	items 					= models.ManyToManyField(OrderProduct)
	start_date 				= models.DateTimeField(auto_now_add=True)
	ordered 				= models.BooleanField(default=False, blank=True)
	sent 					= models.BooleanField(default=False, blank=True)
	received 				= models.BooleanField(default=False, blank=True)
	address 				= models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True) 
	payment 				= models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True) 

	def __str__(self):
		return str(self.user)


	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total



class Address(models.Model):
	user 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
	first_name				= models.CharField(max_length=100)
	last_name				= models.CharField(max_length=100)
	email 					= models.EmailField(verbose_name="email", max_length=60, blank=True)
	street_address			= models.CharField(max_length=100)
	state					= models.CharField(max_length=100)
	city					= models.CharField(max_length=100)
	zip						= models.CharField(max_length=100)
	

	def __str__(self):
		return str(self.user)
		


class Payment(models.Model):
	charge_id = models.CharField(max_length=100)
	user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	amount = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user}'


