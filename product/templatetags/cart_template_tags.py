from django import template
from shop.models import OrderProduct, Customer, Order
from django.shortcuts import render, get_object_or_404

register = template.Library()


@register.filter
def cart_item_count(request, *args, **kwargs):
	if request.user.is_authenticated:
		user = request.user
		try:
			customer, created = Customer.objects.get_or_create(user=user)
			session_key = request.COOKIES['device']
			guest_user = Customer.objects.get(session_key=session_key)
			guest_user_order = OrderProduct.objects.filter(user=guest_user, ordered=False)
			for guest in guest_user_order:
				order_item, created = OrderProduct.objects.update_or_create(
					user=customer,
					item=guest.item,
					quantity=guest.quantity,
					ordered=False,
				)
			order_qs = Order.objects.filter(user=customer, ordered=False)
			if order_qs.exists():
				order = order_qs[0]
				if order.items.filter(item__slug=item.slug).exists():
					order_item.quantity += 1
					order_item.save()
				else:
					order.items.add(order_item)
			else:
				order = Order.objects.create(user=customer)
				order.items.add(order_item)
			# guest_user_order = OrderProduct.objects.filter(user=None)
			# guest_user_order.user = customer
			# guest_user_order.save()
			
			guest_user.delete()
		
		except:
			customer = Customer.objects.get(user=user)
			customer_order = OrderProduct.objects.filter(user=customer, ordered=False)
			for oc in customer_order:
				order_qs = Order.objects.filter(user=customer, ordered=False)
				if order_qs.exists():
					order = order_qs[0]
					order.items.add(oc)
				else:
					order = Order.objects.create(user=customer)
					order.items.add(oc)
			try:
				guest_user = Customer.objects.get(user=None)
				guest_user.delete()
			except:
				pass

		orderitems = OrderProduct.objects.filter(user=customer, ordered=False)
		if orderitems.exists():
			total = sum([item.quantity for item in orderitems])
			return total
	else:
		try:
			session_key = request.COOKIES['device']
		except:
			return '0'
		customer, created = Customer.objects.get_or_create(session_key=session_key)
		orderitems = OrderProduct.objects.filter(user=customer, ordered=False)
		if orderitems.exists():
			total = sum([item.quantity for item in orderitems])
			return total
	return 0




