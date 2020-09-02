'''
Purpose:- extand group user  model 
'''
from datetime import datetime
from django.contrib.auth.models import Group ,GroupManager
from django.db import models
from django.conf import settings

#from simple_history.models import HistoricalRecords
#from core.models import SoftDeleteMixin,SoftDeleteManagerMixin

class UserGroupManager( GroupManager):
	'''
	Define default UserGroupManager 
	return list of camera where is_deleted is False
	'''
	use_in_migrations = True
	
class UserGroup(Group):

	is_deleted = models.BooleanField(default=False, null=False, db_index=True)
	REQUIRED_FIELDS = []
	objects = UserGroupManager() 
	all_objects = models.Manager()
	
	# add Group model history
	
	#Admin side  model name changes
	class Meta:
		verbose_name = 'Group'
		# Display Select verbose_name_plural to change#
		verbose_name_plural = 'Group'
		app_label = 'user'

	def pre_delete_update(self):
		timestamp = datetime.now().timestamp()
		#name has to be unique. Hence to allow the name to be reused, add timestamp to existing
		#name to make it unique.
		self.name = f"{self.name}:{timestamp}"

	def pre_delete_check(self):
		'''
		check if this usergroup can be deleted. UserGroup can be deleted ONLY IF 
		(a) it is not a Super User group
		(b) if there are no child users
		(c) if there are no child camera groups
		'''
		users = self.user_set.all()
		camera_groups =self.cameragroup_set.all()
		
		if self.name is  settings.SUPER_USER_GROUP or  users.exists() is True or camera_groups.exists() is True:
			msg = "Cannot delete User Group as there are undeleted users/camera groups in this group"
			raise models.ProtectedError(msg, list(users)+list(camera_groups))

	def __str__(self):
		return self.name

	# @classmethod
	# def create_superuser_group(cls):
	# 	'''
	# 	If Super User created then super user  add to SuperUser Group by default
	# 	If SuperUser group not exits then create the super user Group
	# 	'''
	# 	super_usergroup_exits=UserGroup.objects.filter(name=settings.SUPER_USER_GROUP).exists()
	# 	if super_usergroup_exits != True:
	# 		UserGroup.objects.create(name=settings.SUPER_USER_GROUP)

	# @classmethod
	# def add_superuser_group(cls,instance):
	# 	if instance.is_superuser :
	# 		super_usergroup=UserGroup.objects.get(name=settings.SUPER_USER_GROUP)
	# 		super_usergroup.user_set.add(instance)
	
	