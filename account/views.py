from django.shortcuts import render, redirect
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from product.models import Category
from account.models import Account, City, State
from product.models import Product, Category, SubCategory
from shop.models import Order, OrderProduct, Customer, Address
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from product.models import Images

class CustomerProductReview(View):
	def get(self, request, *args, **kwargs):
		try:
			cat_menu= Category.objects.all()
			sun_cat_menu= SubCategory.objects.all()

			user = self.request.user
			customer = Customer.objects.get(user=user)
			try:
				order = Order.objects.filter(user=customer, ordered=True)
			except:
				order = None
			try:
				address = Address.objects.filter(user=user)
			except:
				address = None

			try:
				image = Images.objects.filter()
			except:
				image = None

			
			context = {
				'image':image,
				'object':order,
				'address':address,
				'cat_menu':cat_menu,
				'sun_cat_menu':sun_cat_menu,
	
			}
			return render(self.request, 'account/product_review.html', context)
		except ObjectDoesNotExist:
			messages.error(self.request, "You do not have an active account")
			return redirect('product_view')


def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			phone_number = form.cleaned_data.get('phone_number')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(
				phone_number=phone_number, 
				password=raw_password,
			)
			login(request, account)
			return redirect('home')
		else:
			context['registeration_form'] = form
	else:
		form = RegistrationForm()
		context['registeration_form'] = form

	return render(request, 'account/register.html', context)



def login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated: 
		return redirect('home')

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			phone_number = request.POST['phone_number']
			password = request.POST['password']
			user = authenticate(
				phone_number=phone_number, 
				password=password, 
			)
			if user:
				login(request, user)
				return redirect('home')
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)



def login_next(request):
	context = {}
	user = request.user
	if user.is_authenticated: 
		return redirect('home')

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			phone_number = request.POST['phone_number']
			password = request.POST['password']
			user = authenticate(
				phone_number=phone_number, 
				password=password, 
			)
			if user:
				login(request, user)
				return redirect(request.GET.get('next'))
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)

	


def logout_view(request):
	logout(request)
	return redirect('home')



def account_view(request):
	if not request.user.is_authenticated:
		return redirect("login")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, "Account updated")
			return redirect('home')
	else:
		cat_menu = Category.objects.all()
		form = AccountUpdateForm(
			initial={
					"phone_number": request.user.phone_number, 
					"email": request.user.email, 
					"username": request.user.username,
					"first_name": request.user.first_name,
					"last_name": request.user.last_name,
					"street_address": request.user.street_address,
					"zip": request.user.zip,
				}
			)
	context = {
		'account_form':form,
		'cat_menu':cat_menu,
	}

	return render(request, "account/account.html", context)


	

def update_checkout(request):
	if not request.user.is_authenticated:
		return redirect("login")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			context['success_message'] = "Updated"
			return redirect('checkout')
	else:
		form = AccountUpdateForm(
			initial={
					"phone_number": request.user.phone_number, 
					"email": request.user.email, 
					"username": request.user.username,
					"first_name": request.user.first_name,
					"last_name": request.user.last_name,
					"street_address": request.user.street_address,
					"zip": request.user.zip,
			
				}
			)
	context['account_form'] = form
	return render(request, "account/account.html", context)

	

	

def load_cities(request):
	state_id = request.GET.get('state')
	cities = City.objects.filter(state_id=state_id).order_by('name')
	return render(request, 'account/city_dropdown_list_options.html', {'cities': cities})