from django.urls import path
from shop.views import (
	OrderSummaryView,
	Add_To_Cart,
	Add_To_Cart_order_summary,
	remove_single_item_from_cart,
	remove_from_cart,
	CheckoutView,
	PaymentView,
	RequestSentView,
	RequestReceivedFormView
	)

urlpatterns = [
	path('ordersummery', OrderSummaryView.as_view(), name="ordersummery"),
	path('add_to_cart/<slug:slug>', Add_To_Cart, name='add_to_cart'),
	path('add_to_order/<slug:slug>', Add_To_Cart_order_summary, name='add_to_order'),
	path('remove_item_from_cart/<slug:slug>', remove_single_item_from_cart, name='remove_item_from_cart'),
	path('remove_cart/<slug:slug>', remove_from_cart, name='remove_cart'),
	path('checkout', CheckoutView.as_view(), name="checkout"),
	path('payment/', PaymentView.as_view(), name="payment"),
	path('sent/', RequestSentView.as_view(), name="sent"),
	path('received/', RequestReceivedFormView.as_view(), name="received"),
]