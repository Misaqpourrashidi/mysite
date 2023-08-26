from django.urls import path
from account.views import (
	registration_view, 
	login_view,
	logout_view,
	account_view,
	login_next,
	update_checkout,
	load_cities,
	CustomerProductReview
)

urlpatterns = [
	path('register/', registration_view, name="register"),
	path('login/', login_view, name="login"),
	path('logout/', logout_view, name="logout"),
	path('account/', account_view, name="account"),
	path('login_next/', login_next, name="login_next"),
	path('update_checkout/', update_checkout, name="update_checkout"),
	path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
	path('product_view/', CustomerProductReview.as_view(), name="product_view"),
]