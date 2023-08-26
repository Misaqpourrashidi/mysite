from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator


class State(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name 

class City(models.Model):
	state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name



class MyAccountManager(BaseUserManager):
	def create_user(self, phone_number, password):
		if not phone_number:
			raise ValueError('Users must have a Phone Number')
	

		user = self.model(
			phone_number=phone_number,
			
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, password):
		user = self.create_user(
			phone_number=phone_number,

			password=password,
			
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user





class Account(AbstractBaseUser):
	phone_number			= models.CharField(unique=True, max_length=11, validators=[MinLengthValidator(11)])
	email 					= models.EmailField(verbose_name="email", max_length=100, blank=True)
	username 				= models.CharField(unique=False, max_length=30, blank=True)
	first_name				= models.CharField(max_length=30, blank=True)
	last_name				= models.CharField(max_length=30, blank=True)
	street_address			= models.CharField(max_length=100, blank=True)
	zip						= models.CharField(max_length=100, blank=True)
	state 					= models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
	city 					= models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)

	USERNAME_FIELD = 'phone_number'


	objects = MyAccountManager()


	def __str__(self):
		return self.phone_number

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True