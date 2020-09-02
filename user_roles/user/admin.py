from django.contrib import admin

# Register your models here.

from django.contrib.auth import models
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.admin import GroupAdmin as DjangoUserGroupAdmin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from rolepermissions.admin import RolePermissionsUserAdminMixin
from .models import User,UserGroup

#admin.site.unregister(models.Group)

@admin.register(User)
class UserAdmin(DjangoUserAdmin,RolePermissionsUserAdminMixin):
	"""Define admin model for custom User model ."""
	
	fieldsets = (
		(None, {'fields': ('email','username', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','groups')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	readonly_fields = ('last_login','date_joined')
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email','password1','password2',),

		}),
		
	)
	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if db_field.name == "groups":
			kwargs["queryset"] = UserGroup.objects.filter(~Q(is_deleted = True))
		return super().formfield_for_manytomany(db_field, request, **kwargs)

	list_display = ('email', 'first_name', 'last_name', 'is_staff')
	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('email',)

#admin.site.register(UserGroup)
