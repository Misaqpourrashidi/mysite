from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, DeleteView, View
from product.models import Product, Category, SubCategory, Images
from django.urls import reverse_lazy
from product.forms import ImageForm, EditProduct
from django.http import JsonResponse, HttpResponse


def CategoryView(request, slug):
	cat = Category.objects.filter(slug=slug)
	category_products = Product.objects.filter()
	cat_menu = Category.objects.all()
	context = {
		'cats':cat,
		'category_products':category_products,
		'cat_menu':cat_menu,
	}
	return render(request, 'product/category.html', context)


def SubCategoryView(request, slug):
	sub_cat = SubCategory.objects.filter(slug=slug)
	sub_category_products = Product.objects.filter()
	cat_menu= Category.objects.all()
	sub_cat_menu= SubCategory.objects.all()
	context = {
		'sub_cats':sub_cat,
		'sub_category_products':sub_category_products,
		'cat_menu':cat_menu,
		'sub_cat_menu':sub_cat_menu,
	}
	return render(request, 'product/subcategory.html', context)



class ProductDetail(DetailView):
	model = Product
	template_name = 'product/product_detail.html'
	pk_url_kwarg = 'pk'
	slug_url_kwarg = 'slug'
	query_pk_and_slug = True
	imageform = ImageForm

	def post(self, request, *args, **kwargs):
		slug = self.kwargs['slug']
		product = Product.objects.get(slug=slug)
		files = request.FILES.getlist('image')
		imageform = ImageForm(request.POST, request.FILES)

		if imageform.is_valid():
			for file in files:
				Images.objects.create(product=product, image=file)	
			return redirect(reverse("product-detail", kwargs={
				'slug': product.slug
			}))
		else:
			return HttpResponse("The code is wrong")
	
	def get_context_data(self, *args, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		slug = self.kwargs['slug']
		product = Product.objects.filter(slug=slug)

		product_image = Product.objects.get(slug=slug)
		images = Images.objects.filter(product=product_image)

		cat_menu = Category.objects.all()
		sub_cat_menu = SubCategory.objects.all()


		context["sub_cat_menu"] = sub_cat_menu
		context['imageform'] = self.imageform
		context['images'] = images
		context['product'] = product
		context['cat_menu'] = cat_menu
		return context


def DeleteImageForm(request, pk, slug):
	images_form = Images.objects.filter(pk=pk)
	product = Product.objects.get(slug=slug)
	images_form.delete()
	return redirect(reverse("product-detail", kwargs={
		'slug': product.slug
	}))


def UpdateProductView(request, slug):
	context = {}
	product = Product.objects.get(slug=slug)
	if request.POST:
		form = EditProduct(request.POST, request.FILES, instance=product)
		if form.is_valid():
			form.user=user
			form.save()
			return redirect(reverse("product-detail", kwargs={
				'slug': product.slug
			}))
	else:
		product = Product.objects.get(slug=slug)
		form = EditProduct(
			initial={
					"title": product.title, 
					"product_title": product.product_title, 
					"description": product.description,
					"price": product.price,
					"discount_price": product.discount_price,
					"category": product.category,
					"subcategory": product.subcategory,
					"image": product.image,
					"number_product": product.number_product,
				}
			)

	context['form'] = form
	context['product'] = product
	
	return render(request, "product/update_product.html", context)



class DeletePostView(DeleteView):
	model = Product
	pk_url_kwarg = 'pk'
	slug_url_kwarg = 'slug'
	query_pk_and_slug = True
	template_name = 'product/delete_post.html'
	success_url = reverse_lazy('home')