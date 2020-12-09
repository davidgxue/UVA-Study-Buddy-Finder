"""mysite URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from studybuddyfinder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("login/",views.login,name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("register/",views.register, name='register'),
    path("accounts/edit", views.edit, name="edit_account"),
    path('index/', views.index, name='index'),
    path('', views.index),
    path('send-friend-request/<int:id>',views.send_request, name="send-friend-request"),
    path('delete-friend/<int:id>', views.delete_friend, name="delete-friend"),
    path('accept-friend-request/<int:friend_request_id>', views.accept_request, name= "accept-friend-request"),
    path('delete-friend-request/<int:friend_request_id>', views.delete_request, name= "delete-friend-request"),
    path('friends_list/<int:is_creating_group>', views.friends_list, name='friends_list'),
    path('user_list/', views.user_list, name='user_list'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/', views.profile, name='self_profile'),
    path('send-friend-request-profile/<int:id>', views.send_request_profile, name="send-friend-request-profile"),
    path('create_group/', views.create_group, name='create_group'),
    path('group_view/<int:group_id>', views.group_view, name='group_view'),
    path('remove_group_member/<int:group_id>/<int:member_id>', views.remove_group_member, name='remove_group_member'),
    path('add_group_member/<int:group_id>/<int:member_id>', views.add_group_member, name='add_group_member'),
    path('create_announcement/<int:group_id>', views.create_announcement, name='create_announcement'),
    path('remove_announcement/<int:group_id>/<int:announcement_id>', views.remove_announcement, name='remove_announcement'),
    path('add_uva_course/<int:course_id>', views.add_uva_course, name='add_uva_course'),
    path('remove_uva_course/<int:course_id>', views.remove_uva_course, name='remove_uva_course'),
    path('uva_course_list/', views.uva_course_list, name='uva_course_list'),
    path('create_calendar/<int:group_id>', views.create_calendar, name='create_calendar'),
    path('remove_calendar/<int:group_id>/<int:calendar_id>', views.remove_calendar, name='remove_calendar'),
]