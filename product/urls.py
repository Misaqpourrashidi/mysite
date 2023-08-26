from django.urls import path
from product.views import (
	ProductDetail, 
	CategoryView, 
	SubCategoryView,
	DeleteImageForm,
	UpdateProductView,
	DeletePostView
	)


urlpatterns = [
	path('product-detail/<slug:slug>', ProductDetail.as_view(), name="product-detail"),
	path('categorys/<slug:slug>', CategoryView, name="categorys"),
	path('sub_categorys/<slug:slug>', SubCategoryView, name="sub_categorys"),
	path('deleteimageform/<int:pk>/<slug:slug>', DeleteImageForm, name="deleteimageform"),
	path('update_view/<slug:slug>', UpdateProductView, name="update_view"),
	path('delete_view/<slug:slug>', DeletePostView.as_view(), name="delete_view"),
]