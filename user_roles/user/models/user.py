"""Declare models for new user creation ."""

from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
#from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _


from .user_group import UserGroup

class UserManager(BaseUserManager):
	"""Define a model manager for User model with no username field."""

	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""Create and save a User with the given email and password."""
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, **extra_fields):
		"""Create and save a regular User with the given email and password."""
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		"""Create and save a SuperUser with the given email and password."""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)

	def get_queryset(self):
		'''
		Define default get_queryset 
		return list of user where is_deleted is False
		'''
		return super(UserManager, self).get_queryset().filter(is_deleted=False)

class User(AbstractUser):
	"""User model."""
	email = models.EmailField(_('email address'), unique=True)
	is_deleted = models.BooleanField(default=False, null=False, db_index=True)
	
	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'email'
	
	objects = UserManager()
	# add user model history
	

	#Admin side  model name changes
	class Meta:
		verbose_name = 'User'
		# Display Select verbose_name_plural to change#
		verbose_name_plural = 'User'
		app_label = 'user'

	def save(self, *args, **kwargs):
		self.username=self.email
		super(User, self).save(*args, **kwargs)