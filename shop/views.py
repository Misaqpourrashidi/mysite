from product.models import Product
from shop.models import OrderProduct, Order, Customer, Address, Payment
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.forms import CheckoutForm, CheckOutUpdateForm, SentForm, ReceivedForm
import random
import string

def create_ref_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


	
class OrderSummaryView(View):
	def get(self, request, *args, **kwargs):	
		if self.request.user.is_authenticated:
			try:
				user = self.request.user
				customer = Customer.objects.get(user=user)
				try:
					order = Order.objects.get(user=customer, ordered=False)
				except:
					order = None

				try:
					order_product = OrderProduct.objects.filter(user=customer, ordered=False)
				except:
					order_product = None
	
				context = {
					'order_product':order_product,
					'object': order
				}
				return render(self.request, 'shop/ordersummary.html', context)
			except ObjectDoesNotExist:
				messages.error(self.request, "You do not have an active account")
				return redirect('home')
		else:
			try:
				session_key = self.request.COOKIES['device']
				customer, created = Customer.objects.get_or_create(session_key=session_key)
				try:
					order = Order.objects.get(user=customer, ordered=False)
				except:
					order = None
				try:
					order_product = OrderProduct.objects.filter(user=customer, ordered=False)
				except:
					order_product = None

				context = {
					'order_product':order_product,
					'object': order
				}
				return render(self.request, 'shop/ordersummary.html', context)
			except ObjectDoesNotExist:
				messages.error(self.request, "You do not have an active account")
				return redirect('home')



def Add_To_Cart(request, slug):
	if request.user.is_authenticated:
		item = get_object_or_404(Product, slug=slug)
		item.number_product -= 1
		item.save()
		user = request.user
		customer = Customer.objects.get(user=user)
		order_item, created = OrderProduct.objects.get_or_create(
			item=item,
			user=customer,
			ordered = False
		)
		order_qs = Order.objects.filter(user=customer, ordered=False)
		if order_qs.exists():
			order = order_qs[0]
		    # check if the order post is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item.quantity += 1
				order_item.save()
				messages.success(request, "this item just added to your cart")
				return redirect('product-detail', slug=slug)
			else:
				order.items.add(order_item)
				messages.success(request, "this item just added to your cart")
				return redirect('product-detail', slug=slug)
		else:
			order = Order.objects.create(user=customer)
			order.items.add(order_item)
		messages.success(request, "this item just added to your cart")
		return redirect('product-detail', slug=slug)
	else:
		item = get_object_or_404(Product, slug=slug)
		item.number_product -= 1
		item.save()
		session_key = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(session_key=session_key)
		order_item, created = OrderProduct.objects.get_or_create(
			item=item,
			user=customer,
			ordered = False
		)
		order_qs = Order.objects.filter(user=customer, ordered=False)
		if order_qs.exists():
			order = order_qs[0]
		    # check if the order post is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item.quantity += 1
				order_item.save()
				messages.success(request, "this item just added to your cart")
				return redirect('product-detail', slug=slug)
			else:
				order.items.add(order_item)
				messages.success(request, "this item just added to your cart")
				return redirect('product-detail', slug=slug)
		else:
			order = Order.objects.create(user=customer)
			order.items.add(order_item)
		messages.success(request, "this item just added to your cart")
		return redirect('product-detail', slug=slug)




def Add_To_Cart_order_summary(request, slug):
	if request.user.is_authenticated:
		user = request.user
		customer = Customer.objects.get(user=user)
		item = get_object_or_404(Product, slug=slug)
		order_item, created = OrderProduct.objects.get_or_create(
			item=item,
			user=customer,
			ordered = False
		)
		order_qs = Order.objects.filter(user=customer, ordered=False)
		if order_qs.exists():
			order = order_qs[0]
	    	# check if the order post is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item.quantity += 1
				order_item.save()
				messages.info(request, "this item just updated")
				return redirect('ordersummery')
			else:
				order.items.add(order_item)
				messages.info(request, "this item just updated")
				return redirect('ordersummery')
	else:
		session_key = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(session_key=session_key)
		item = get_object_or_404(Product, slug=slug)
		order_item, created = OrderProduct.objects.get_or_create(
			item=item,
			user=customer,
			ordered = False
		)
		order_qs = Order.objects.filter(user=customer, ordered=False)
		if order_qs.exists():
			order = order_qs[0]
	    	# check if the order post is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item.quantity += 1
				order_item.save()
				messages.info(request, "this item just updated")
				return redirect('ordersummery')
			else:
				order.items.add(order_item)
				messages.info(request, "this item just updated")
				return redirect('ordersummery')
	messages.info(request, "this item just updated")	
	return redirect('ordersummery')


def remove_single_item_from_cart(request, slug):
	if request.user.is_authenticated:
		item = get_object_or_404(Product, slug=slug)
		user = request.user
		customer = Customer.objects.get(user=user)
		order_qs = Order.objects.filter(
			user=customer,
			ordered = False
		)
		if order_qs.exists():
			order = order_qs[0]
	    	# check if the order post is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item = OrderProduct.objects.filter(
					item=item,
					user=customer,
					ordered=False
				)[0]
				if order_item.quantity > 1:
					order_item.quantity -= 1
					order_item.save()
				else:
					order_item.delete()
				messages.warning(request, "this item just updated")	
				return redirect('ordersummery')
			else:
				messages.warning(request, "this item just updated")	
				return redirect('product-detail', slug=slug)
	else:
		item = get_object_or_404(Product, slug=slug)
		session_key = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(session_key=session_key)
		order_qs = Order.objects.filter(
			user=customer,
			ordered = False
		)
		if order_qs.exists():
			order = order_qs[0]
	    	# check if the order post is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item = OrderProduct.objects.filter(
					item=item,
					user=customer,
					ordered=False
				)[0]
				if order_item.quantity > 1:
					order_item.quantity -= 1
					order_item.save()
				else:
					order_item.delete()
				messages.warning(request, "this item just updated")	
				return redirect('ordersummery')
			else:
				messages.warning(request, "this item just updated")	
				return redirect('product-detail', slug=slug)


def remove_from_cart(request, slug):
	if request.user.is_authenticated:
		item = get_object_or_404(Product, slug=slug)
		user = request.user
		customer = Customer.objects.get(user=user)
		order_qs = Order.objects.filter(
			user=customer,
			ordered = False
		)
		if order_qs.exists():
			order = order_qs[0]
	    	# check if the order post is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item = OrderProduct.objects.filter(
					item=item,
					user=customer,
					ordered=False
				)[0]
				
				order_item.delete()
				messages.warning(request, "this item was removed")
				return redirect('ordersummery')
			else:
				messages.warning(request, "this item was removed")
				return redirect('product-detail', slug=slug)
	else:
		item = get_object_or_404(Product, slug=slug)
		session_key = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(session_key=session_key)
		order_qs = Order.objects.filter(
			user=customer,
			ordered = False
		)
		if order_qs.exists():
			order = order_qs[0]
	    	# check if the order post is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item = OrderProduct.objects.filter(
					item=item,
					user=customer,
					ordered=False
				)[0]
				
				order_item.delete()
				messages.warning(request, "this item was removed")
				return redirect('ordersummery')
			else:
				messages.warning(request, "this item was removed")
				return redirect('product-detail', slug=slug)


class CheckoutView(LoginRequiredMixin,View):
	login_url = 'login_next'
	redirect_field_name = 'next'
	def get(self, request,*args, **kwargs):
		try:
			user = self.request.user
			customer, created = Customer.objects.get_or_create(user=user)
			order = Order.objects.get(user=customer, ordered=False)
			
			form = CheckoutForm(
				initial={
						"phone_number": self.request.user.phone_number, 
						"email": self.request.user.email, 
						"first_name": self.request.user.first_name,
						"last_name": self.request.user.last_name,
						"street_address": self.request.user.street_address,
						"zip": self.request.user.zip,
					}
				)

			form1 = CheckOutUpdateForm(
				initial={
					"city": request.user.city,
				}
			)
		
			context = {
				'form1':form1,
				'account_form':form,
				'order': order,		
			}
			return render(self.request, 'shop/checkout.html', context)
		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an active order")
			return redirect('checkout')

	def post(self, request, *args, **kwargs):		
		form = CheckOutUpdateForm(request.POST, instance=request.user)
		form1 = CheckoutForm(self.request.POST or None)
		try:
			user = self.request.user
			customer, created = Customer.objects.get_or_create(user=user)
			order = Order.objects.get(user=customer, ordered=False)
			if form1.is_valid():
				form.save()
				payment_option = form1.cleaned_data.get('payment_option')
				address = Address(
						user = user,
						first_name = self.request.user.first_name,
						last_name = self.request.user.last_name,
						email = self.request.user.email,
						street_address = self.request.user.street_address,
						zip = self.request.user.zip,
						state = self.request.user.state,
						city = self.request.user.city,
					)

				address.save()
				order.address = address
				order.save()

				return redirect('payment')
				messages.success(self.request, "All Good")
			messages.warning(self.request, "Invalid Payment Options")
			return redirect('checkout')
		except ObjectDoesNotExist:
			messages.error(self.request, "You do not have an active account")
			return redirect('/ordersummery/')




class PaymentView(View):
	def get(self, *args, **kwargs):
		return render(self.request, 'shop/payment.html')
	def post(self, *args, **kwargs):
		user = self.request.user
		customer = Customer.objects.get(user=user)
		order = Order.objects.get(user=customer, ordered=False)



		# create Payment
		payment = Payment()
		payment.charge_id = '4654646449789'
		payment.amount = order.get_total()
		payment.user = customer
		payment.save()

		# assign the order to the payment
		
		order_item = order.items.all()
		order_item.update(ordered = True)
		for item in order_item:
			item.save()

		order.ordered = True
		order.payment = payment

		order.ref_code = create_ref_code()
		order.save()

		messages.success(self.request, "Payment Was Seccess Full")
		return redirect('product_view')



class RequestSentView(View):
	def get(self, *args, **kwargs):
		form = SentForm()
		context = {
			'form':form
		}
		return render(self.request, 'shop/sent.html', context)
	def post(self, *args, **kwargs):
		form = SentForm(self.request.POST)
		if form.is_valid():

			ref_code = form.cleaned_data.get('ref_code')

			try:
				order = Order.objects.get(ref_code=ref_code)
				order.sent = True
				order.save()


				messages.success(self.request, 'your request is done')
				return redirect('sent')

			except ObjectDoesNotExist:
				messages.error(self.request, 'your order does not exist')
				return redirect('sent')


class RequestReceivedFormView(View):
	def get(self, *args, **kwargs):
		form = ReceivedForm()
		context = {
			'form':form
		}
		return render(self.request, 'shop/received.html', context)
	def post(self, *args, **kwargs):
		form = ReceivedForm(self.request.POST)
		if form.is_valid():

			ref_code = form.cleaned_data.get('ref_code')

			try:
				order = Order.objects.get(ref_code=ref_code)
				order.received = True
				order.save()


				messages.success(self.request, 'your request is done')
				return redirect('received')

			except ObjectDoesNotExist:
				messages.info(self.request, 'your order does not exist')
				return redirect('received')