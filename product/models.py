from django.db import models
from django.shortcuts import render, redirect, reverse

from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
import random
import string

def create_randon_number():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


class Category(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=350, unique=True, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)



def slugify_instance_category(instance, save=False, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.name)
	qs = Category.objects.filter(slug=slug).exclude(id=instance.id)
	if qs.exists():
		slug = f"{slug}-{create_randon_number()}"
		return slugify_instance_category(instance, save=save, new_slug=slug)
	instance.slug = slug
	if save:
		instance.save()
	return instance 

def product_pre_save(sender, instance, *args, **kwargs):
	if instance.slug is None:
		slugify_instance_category(instance, save=False)

pre_save.connect(product_pre_save, sender=Category)

def product_post_save(sender, instance, created, *args, **kwargs):
	if created:
		slugify_instance_category(instance, save=True)

post_save.connect(product_post_save, sender=Category)


class SubCategory(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=350, unique=True, blank = True)

	def __str__(self):
		return f"{self.name} OF {self.category.name}"

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

def slugify_instance_subcategory(instance, save=False, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.name)
	qs = SubCategory.objects.filter(slug=slug).exclude(id=instance.id)
	if qs.exists():
		slug = f"{slug}-{create_randon_number()}"
		return slugify_instance_subcategory(instance, save=save, new_slug=slug)
	instance.slug = slug
	if save:
		instance.save()
	return instance 

def product_pre_save(sender, instance, *args, **kwargs):
	if instance.slug is None:
		slugify_instance_subcategory(instance, save=False)

pre_save.connect(product_pre_save, sender=SubCategory)

def product_post_save(sender, instance, created, *args, **kwargs):
	if created:
		slugify_instance_subcategory(instance, save=True)

post_save.connect(product_post_save, sender=SubCategory)



class Product(models.Model):
	title = models.CharField(max_length=200)
	product_title = models.CharField(max_length=400)
	description = models.TextField()
	price = models.FloatField()
	discount_price = models.FloatField(blank=True, null=True)
	image = models.ImageField(null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
	slug = models.SlugField(max_length=350, unique=True, blank=True)
	check = models.BooleanField(blank=True, default=False)
	number_product = models.FloatField()

	def __str__(self):
		return self.product_title


	def get_add_to_cart(self):
		return reverse('add_to_cart', kwargs={'slug':self.slug})


	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = 'static/images/no-image.png'
		return url

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)



def slugify_instance_product_title(instance, save=False, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.product_title)
	qs = Product.objects.filter(slug=slug).exclude(id=instance.id)
	if qs.exists():
		slug = f"{slug}-{create_randon_number()}"
		return slugify_instance_product_title(instance, save=save, new_slug=slug)
	instance.slug = slug
	if save:
		instance.save()
	return instance 

def product_pre_save(sender, instance, *args, **kwargs):
	if instance.slug is None:
		slugify_instance_product_title(instance, save=False)

pre_save.connect(product_pre_save, sender=Product)

def product_post_save(sender, instance, created, *args, **kwargs):
	if created:
		slugify_instance_product_title(instance, save=True)

post_save.connect(product_post_save, sender=Product)





class Images(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	image = models.ImageField(null=True, blank=True, upload_to="images/")

	def __str__(self):
		return self.product.product_title