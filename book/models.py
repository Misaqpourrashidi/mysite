from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import URLValidator
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
from w_date.models import (
	January,
	February,
	March,
	April,
	May,
	June,
	July,
	August,
	September,
	October,
	November,
	December,
)

import random
import string

def create_randon_number():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

class Book(models.Model):
	first_name = models.CharField(max_length=255, blank=True)
	last_name = models.CharField(max_length=255, blank=True)
	phone_number = models.CharField(max_length=11, validators=[MinLengthValidator(11)], blank=True)
	email = models.EmailField(verbose_name="email", max_length=60, blank=True)
	address = models.CharField(max_length=100, blank=True)
	website = models.CharField(max_length=100, validators=[URLValidator()], blank=True)
	summary = RichTextField(blank=True, null=True)
	experience = RichTextField(blank=True, null=True)
	education = RichTextField(blank=True, null=True)
	skills = RichTextField(blank=True, null=True)
	background = models.ImageField(null=True, blank=True, upload_to="images/")
	image = models.ImageField(null=True, blank=True, upload_to="images/")
	december = models.ForeignKey(December, on_delete=models.SET_NULL, null=True, blank=True)
	january = models.ForeignKey(January, on_delete=models.SET_NULL, null=True, blank=True)
	april = models.ForeignKey(April, on_delete=models.SET_NULL, null=True, blank=True)
	february = models.ForeignKey(February, on_delete=models.SET_NULL, null=True, blank=True)
	march = models.ForeignKey(March, on_delete=models.SET_NULL, null=True, blank=True)
	may = models.ForeignKey(May, on_delete=models.SET_NULL, null=True, blank=True)
	june = models.ForeignKey(June, on_delete=models.SET_NULL, null=True, blank=True)
	july = models.ForeignKey(July, on_delete=models.SET_NULL, null=True, blank=True)
	august = models.ForeignKey(August, on_delete=models.SET_NULL, null=True, blank=True)
	september = models.ForeignKey(September, on_delete=models.SET_NULL, null=True, blank=True)
	october = models.ForeignKey(October, on_delete=models.SET_NULL, null=True, blank=True)
	november = models.ForeignKey(November, on_delete=models.SET_NULL, null=True, blank=True)
	slug = models.SlugField(max_length=25, blank=True, unique=True)

	def __str__(self):
		return f'DR.{self.first_name} {self.last_name}'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

def slugify_instance_book_title(instance, save=False, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(f"{instance.first_name} {instance.last_name}")

	qs = Book.objects.filter(slug=slug).exclude(id=instance.id)
	if qs.exists():
		slug = f"{slug}-{create_randon_number()}"
		return slugify_instance_book_title(instance, save=save, new_slug=slug)
	instance.slug = slug
	if save:
		instance.save()
	return instance 

def product_pre_save(sender, instance, *args, **kwargs):
	if instance.slug is None:
		slugify_instance_book_title(instance, save=False)

pre_save.connect(product_pre_save, sender=Book)

def product_post_save(sender, instance, created, *args, **kwargs):
	if created:
		slugify_instance_book_title(instance, save=True)

post_save.connect(product_post_save, sender=Book)



class Comment(models.Model):
	CommentPost = models.ForeignKey(Book , on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	content = models.TextField()
	date_posted = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering=['-date_posted']

	def __str__(self):
		return str(self.content) + str(self.id)

	

class Parent(models.Model):
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
	name_reply = models.CharField(max_length=30)
	content_reply = models.TextField()


	def __str__(self):
		return f'DR.{self.comment} {self.id}'