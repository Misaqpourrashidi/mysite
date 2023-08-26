from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from product.models import Product, Category, SubCategory
from book.forms import CommentForm, CommentChilderenForm
from book.models import Book, Comment, Parent
from w_date.models import (
	January, 
	Month_Name,
	Year,
)


class HomeView(ListView):
	model = Product
	template_name = 'book/home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(HomeView, self).get_context_data(*args, **kwargs)
		product = Product.objects.filter(check=True)[0:3]

		sub_cat_menu= SubCategory.objects.all()
		cat_menu = Category.objects.all()


		context["product"] = product
		context["cat_menu"] = cat_menu
		context["sub_cat_menu"] = sub_cat_menu
		return context



class CalendarView(ListView):
	model = Book
	template_name = 'book/calendar.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CalendarView, self).get_context_data(*args, **kwargs)
		year= Year.objects.all()
		month_name= Month_Name.objects.all()
		january= January.objects.all()
		book = Book.objects.all()
		cat_menu= Category.objects.all()
		sun_cat_menu= SubCategory.objects.all()

		context["years"] = year
		context["month_names"] = month_name
		context["januarys"] = january
		context["books"] = book
		context["cat_menu"] = cat_menu
		context["sun_cat_menu"] = sun_cat_menu
		return context


class ArticleDetailView(DetailView):
	model = Book
	template_name = 'book/article_detail.html'
	pk_url_kwarg = 'pk'
	slug_url_kwarg = 'slug'
	query_pk_and_slug = True

	def get_context_data(self, *args, **kwargs):
		context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

		connected_comments = Comment.objects.filter(CommentPost=self.get_object())
		number_of_comments = connected_comments.count()

		cat_menu= Category.objects.all()
		sun_cat_menu= SubCategory.objects.all()
		slug = self.kwargs['slug']
		book = Book.objects.filter(slug=slug)

		parent = Parent.objects.all()
		
		context["parent"] = parent
		context["book"] = book
		context["cat_menu"] = cat_menu
		context["sun_cat_menu"] = sun_cat_menu
		context['comments'] = connected_comments
		context['comment_form'] = CommentForm()
		

		context['no_of_comments'] = number_of_comments
		return context

	def post(self , request , *args , **kwargs):
		comment_form = CommentForm(self.request.POST)
		form = CommentChilderenForm(self.request.POST)
		book = self.get_object()

		if comment_form.is_valid():
			name = comment_form.cleaned_data['name']
			content = comment_form.cleaned_data['content']


			new_comment = Comment(name=name, content=content , CommentPost=self.get_object())
			new_comment.save()
			return redirect(reverse("article-detail", kwargs={
				'slug': book.slug
			}))

		if form.is_valid():
			name_reply = form.cleaned_data['name_reply']
			content_reply = form.cleaned_data['content_reply']
			comment = form.cleaned_data['comment']
			
			parent = Parent(name_reply=name_reply, content_reply=content_reply, comment=comment)
			parent.save()
			return redirect(reverse("article-detail", kwargs={
				'slug': book.slug
			}))





def delete_comment(request, pk, slug):
	comment = Comment.objects.filter(pk=pk)
	book = Book.objects.get(slug=slug)
	comment.delete()
	return redirect(reverse("article-detail", kwargs={
		'slug': book.slug
	}))



def delete_reply(request, pk, slug):
	parent = Parent.objects.filter(pk=pk)
	book = Book.objects.get(slug=slug)
	parent.delete()
	return redirect(reverse("article-detail", kwargs={
		'slug': book.slug
	}))