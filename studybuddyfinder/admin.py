from django.contrib import admin
from .models import UserProfile, FriendRequest, Group, Announcement, Course, Calendar

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FriendRequest)
admin.site.register(Group)
admin.site.register(Announcement)
admin.site.register(Course)
# Adding model
admin.site.register(Calendar)