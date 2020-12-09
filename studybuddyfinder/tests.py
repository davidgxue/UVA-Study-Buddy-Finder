from django.test import TestCase, Client, RequestFactory
from .models import UserProfile,User,FriendRequest, Group, Announcement, Calendar
from django.urls import reverse
from .views import register, send_request, user_list,delete_request,friends_list,create_group, add_group_member, remove_group_member, group_view, index, login, logout_view, edit, profile, create_announcement, remove_announcement, create_calendar, remove_calendar
from .forms import SearchForm, CreateUserProfileForm, EditUserProfileForm
# Create your tests here.


class UserProfileTesting(TestCase):
    def setUp(self):
        current_user = UserProfile(school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
    def test_profileTest(self):
        current_user = UserProfile(school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.assertEqual(current_user.year, 2)
    def test_profileTest1(self):
        current_user = UserProfile(school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.assertEqual(current_user.major, 'CS')
    def test_profileTest2(self):
        current_user = UserProfile(school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.assertEqual(current_user.city, 'Charlottesville')
    def test_profileTest3(self):
        current_user = UserProfile(school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.assertEqual(current_user.state, 'VA')
    def test_profileTest4(self):
        current_user = UserProfile(school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.assertEqual(current_user.school, 'UVA')
    def test_profileTest5(self):
        current_user = UserProfile(school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.assertEqual(current_user.discord_id, '1234')
    def test_profileTest6(self):
        current_user = UserProfile(school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.assertEqual(current_user.zoom_id, '1234567890')
    def student_verification_Test1(self):
        current_user = UserProfile(email='123@virginia.edu', school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2, student_verified=True)
        self.assertEqual(current_user.student_verified, True)
    def student_verification_Test2(self):
        current_user = UserProfile(email='123@gmail.com', school='UVA', major='CS', state='VA', city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2, student_verified=True)
        self.assertEqual(current_user.student_verified, False)


class UserListDisplayTesting(TestCase):
   def setUp(self):
       self.request_factory = RequestFactory()
       self.user = User.objects.create(username='Testuser', id=2)
       self.userProf = UserProfile(user=self.user, user_id=2, school='UVA', major='CS', state='VA',
                                   city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
       self.userProf.save()
   def test_view_url_exists_at_desired_location(self):
       request = RequestFactory().get('/')
       request.user = self.user
       request.user_id = 1
       response = user_list(request)
       self.assertEqual(response.status_code, 200)


class FriendshipTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        # make user1
        self.user = User.objects.create(username='Testuser', id=1)
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA',
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()

        # make user2
        self.user2 = User.objects.create(username='Testuser2', id=2)
        self.userProf2 = UserProfile(user=self.user2, school='UVA', major='CS', state='VA',
                                     city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf2.save()

        # make user3
        self.user3 = User.objects.create(username='Testuser3', id=3)
        self.userProf3 = UserProfile(user=self.user3, school='UVA', major='CS', state='VA',
                                     city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf3.save()

    def test_view_url_exists_at_desired_location(self):
        request = RequestFactory().get('/')
        request.user = self.user
        request.user_id = 1
        response = friends_list(request,0)
        self.assertEqual(response.status_code, 200)

    def test_add_friend_request_when_friend_exists(self):
        #friend request sent from user1 to user2
        request = RequestFactory()
        request.user = self.user
        response = send_request(request, self.user2.id)

        friend_request = FriendRequest.objects.get(to_user=self.userProf2)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(friend_request)

    def test_add_friend_request_when_friend_doesnt_exists(self):
        #friend request sent from user1 to user5 who doesnt exist
        request = RequestFactory()
        request.user = self.user
        response = send_request(request, "5")
        friend_request = FriendRequest.objects.all().count()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(friend_request ==0)

    def test_add_then_delete_friend_request(self):
        request = RequestFactory()
        request.user = self.user
        response = send_request(request, "2")
        friend_request_id = FriendRequest.objects.first().id
        response2= delete_request(request,friend_request_id)
        friend_requests_length = FriendRequest.objects.all().count()
        self.assertTrue(friend_requests_length == 0)

    def test_delete_friend_request_when_friend_doesnt_exist(self):
        request = RequestFactory()
        request.user = self.user
        #response = send_request(request, "2")
        try:
            friend_request_id = FriendRequest.objects.first().id
            response2= delete_request(request,friend_request_id)
            friend_requests_length = FriendRequest.objects.all().count()
        except:
            return True


class GroupTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        # make user1
        self.user = User.objects.create(username='Testuser')
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()

        # make user2
        self.user2 = User.objects.create(username='Testuser2')
        self.userProf2 = UserProfile(user=self.user2, school='UVA', major='CS', state='VA', id=2,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf2.save()
        #make group 1
        self.group= Group.objects.create(name = "Group1", owner = self.userProf) # i removed id



    def test_create_group(self):
        request = RequestFactory().post('/create_group/', {'group_name': "test group"})
        request.user = self.user
        response = create_group(request)
        self.assertTrue(Group.objects.get(name= "test group"))

    def test_add_to_group_responding(self): #
        request = RequestFactory().get('/')
        request.user = self.user
        request.user_id = 1
        response = add_group_member(request, self.group.id ,2)
        self.assertEqual(response.status_code, 302)


    def test_add_to_group_as_owner(self): #
        request = RequestFactory().get('/')
        request.user = self.user
        request.user_id = 1
        response = add_group_member(request,  self.group.id, 2)
        self.assertEqual(self.group.members.all().count(), 1)

    def test_create_group_on_friends_list_url_responding(self):
        request = RequestFactory().get('/')
        request.user = self.user
        request.user_id = 1
        response = friends_list(request,1)
        self.assertEqual(response.status_code, 200)


    def test_group_view_page_is_responding(self): #
        request = RequestFactory().get('/')
        request.user = self.user
        request.user_id = 1
        response = group_view(request,self.group.id)
        self.assertEqual(response.status_code, 200)

    def test_group_view_page_doesnt_respond_on_false_group(self):
        try:
            request = RequestFactory().get('/')
            request.user = self.user
            request.user_id = 1
            response = group_view(request, 200)

        except:
            return True


    def test_remove_group_member(self): #
        request = RequestFactory().get('/')
        request.user = self.user
        request.user_id = 1
        add_group_member(request, self.group.id, 2)
        remove_group_member(request, self.group.id ,2)
        self.assertEqual(self.group.members.all().count(), 0)

    def test_remove_group_member_throws_error_on_false_user(self):
        try:
            request = RequestFactory().get('/')
            request.user = self.user
            request.user_id = 1
            remove_group_member(request, 1, 2)

        except:
            return True


class RestrictToUsersTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username='Testuser')
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()
        self.user2 = User.objects.create(username='Testuser2')
        self.userProf2 = UserProfile(user=self.user2, school='UVA', major='CS', state='VA', id=2,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf2.save()

    def test_view_url_exists_at_desired_location(self):
       request = RequestFactory().get('/')
       request.user = self.user
       request.user_id = 1
       response = user_list(request)
       self.assertEqual(response.status_code, 200)
    
    def test_user_list_displays_unfiltered(self):
        request = RequestFactory().get('/')
        request.user = self.user
        response = user_list(request)
        num_users = UserProfile.objects.all().count()
        self.assertTrue(num_users==2)


class AccountTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username='Testuser')
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()
        self.user2 = User.objects.create(username='Testuser2')
        self.userProf2 = UserProfile(user=self.user2, school='UVA', major='CS', state='VA', id=2,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf2.save()

    def test_register_works(self):
       request = RequestFactory().get('/')
       test = User.objects.create(username='Tests')
       request.user = test
       request.user_id = 1
       response = register(request)
       self.assertEqual(response.status_code, 200)
    
    def test_register_throws_error_if_not_valid_input(self):
       request = RequestFactory().get('/')
       try:
            self.user = User.objects.create(username='Testuser')
            self.userProf = UserProfile(user=self.user, major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
            self.userProf.save()
       except:
           return True
    
    def test_edit_works(self):
       request = RequestFactory().get('/')
       request.user = self.user
       request.user_id = 1
       response = edit(request)
       self.assertEqual(response.status_code, 200)
    
    def test_user_list_works(self):
       request = RequestFactory().get('/')
       request.user = self.user
       request.user_id = 1
       response = user_list(request)
       self.assertEqual(response.status_code, 200)

    def test_friends_list_works(self):
       request = RequestFactory().get('/')
       request.user = self.user
       request.user_id = 1
       response = friends_list(request, 1)
       self.assertEqual(response.status_code, 200)

    def test_profile_works(self):
       request = RequestFactory().get('/')
       request.user = self.user
       request.user_id = 1
       response = profile(request, "2")
       self.assertEqual(response.status_code, 200)
    

class SearchFilterTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username='Testuser')
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()

    def test_restrict_by_school(self):
        form = SearchForm(data={"restrict_school" : "College of Arts & Sciences"})
        self.assertEqual(form.errors, {})

    def test_restrict_by_year(self):
        form = SearchForm(data={"restrict_year" : "First Year"})
        self.assertEqual(form.errors, {})

    def test_restrict_by_major(self):
         form = SearchForm(data={"restrict_major" : "Computer Science"})
         self.assertEqual(form.errors, {})

    def test_restrict_by_all(self):
         form = SearchForm(data={"restrict_year" : "Second Year", "restrict_school" : "College of Arts & Sciences", "restrict_major" : "Computer Science"})
         self.assertEqual(form.errors, {})
    
    def test_restrict_by_school_works(self):
         request = RequestFactory().post('/')
         request.user = self.user
         request.user_id = 1
         form = SearchForm(data={"restrict_school" : "College of Arts & Sciences"})
         self.assertEqual(form.errors, {}) 
    
    def test_restrict_by_year_works(self):
         request = RequestFactory().post('/')
         request.user = self.user
         request.user_id = 1
         form = SearchForm(data={"restrict_year" : "First Year"})
         self.assertEqual(form.errors, {}) 

    def test_restrict_by_major_works(self):
         request = RequestFactory().post('/')
         request.user = self.user
         request.user_id = 1
         form = SearchForm(data={"restrict_major" : "Computer Science"})
         self.assertEqual(form.errors, {}) 
    
    def test_restrict_by_all_works(self):
         request = RequestFactory().post('/')
         request.user = self.user
         request.user_id = 1
         form = SearchForm(data={"restrict_major" : "Computer Science", "restrict_year" : "Second Year", "restrict_school" : "College of Arts & Sciences"})
         self.assertEqual(form.errors, {}) 
         

class FormsTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username='Testuser')
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()

    def test_create_user_profile_form_throws_error(self):
         form = CreateUserProfileForm(data={"hide_major":True, 'city':"Charlottesville", 'hide_school':False, 'major':"Computer Science",'hide_major':False, 'state':"Virginia",'hide_state':True, 'year':'Second Year','hide_year':False,'discord_id':'xyz','zoom_id':'qwerty'})
         self.assertEqual(form.errors, {'school': ['This field is required.']})

    def test_create_user_profile_form_works(self):
         form = CreateUserProfileForm(data={"hide_major":True, 'school':"College of Arts & Sciences", 'city':"Charlottesville", 'hide_school':False, 'major':"Computer Science",'hide_major':False, 'state':"Virginia",'hide_state':True, 'year':'Second Year','hide_year':False,'discord_id':'xyz','zoom_id':'qwerty'})
         self.assertEqual(form.errors, {})

    def test_edit_user_profile_form_throws_error(self):
         form = EditUserProfileForm(data={"hide_major":True, 'city':"Charlottesville", 'hide_school':False, 'major':"Computer Science",'hide_major':False, 'state':"Virginia",'hide_state':True, 'year':'Second Year','hide_year':False,'discord_id':'xyz','zoom_id':'qwerty'})
         self.assertEqual(form.errors, {'school': ['This field is required.']})

    def test_edit_user_profile_form_works(self):
         form = EditUserProfileForm(data={"hide_major":True, 'school':"College of Arts & Sciences", 'city':"Charlottesville", 'hide_school':False, 'major':"Computer Science",'hide_major':False, 'state':"Virginia",'hide_state':True, 'year':'Second Year','hide_year':False,'discord_id':'xyz','zoom_id':'qwerty'})
         self.assertEqual(form.errors, {})

    def test_search_form_doesnt_throw_error(self):
        form = SearchForm(data={})
        self.assertEqual(form.errors, {})

    def test_search_form_works(self):
        form = SearchForm(data={"restrict_major": "Computer Science"})
        self.assertEqual(form.errors, {})


class UrlTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username='Testuser')
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()

    # def test_user_list_url_config(self):
    #     response = self.client.get(reverse('user_list'))
    #     self.assertEqual(response.status_code, 302)

    # def test_register_url_config(self):
    #     response = self.client.get(reverse('register'))
    #     self.assertEqual(response.status_code, 200)
    
    # def test_logout_url_config(self):
    #     response = self.client.get(reverse('logout'))
    #     self.assertEqual(response.status_code, 302)

    # def test_user_list_url_template(self):
    #     response = self.client.get(reverse('user_list'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'studybuddyfinder/user_list.html')

    # def test_user_list_template_used_in_filter1(self):
    #     form = SearchForm(data={})
    #     self.assertEqual(form.errors, {})
    #     response = self.client.get(reverse('user_list'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'studybuddyfinder/index.html')

    # def test_user_list_template_used_in_filter2(self):
    #     form = SearchForm(data={'restrict_school':True})
    #     self.assertEqual(form.errors, {})
    #     response = self.client.get(reverse('user_list'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'studybuddyfinder/user_list.html')
    # def test_user_list_template_used_in_filter3(self):
    #     form = SearchForm(data={'restrict_school':True, 'restrict_year':True, 'restrict_major':True})
    #     self.assertEqual(form.errors, {})
    #     response = self.client.get(reverse('user_list'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'studybuddyfinder/user_list.html')


class AnnouncementTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        # make user1
        self.user = User.objects.create(username='Testuser')
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()

        # make user2
        self.user2 = User.objects.create(username='Testuser2')
        self.userProf2 = UserProfile(user=self.user2, school='UVA', major='CS', state='VA', id=2,
                                     city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf2.save()
        # make group 1
        self.group = Group.objects.create(name="Group1", owner=self.userProf)

    def test_create_announcement (self):
        request = RequestFactory().post('/create_announcement/', {'message': "test message"})
        request.user = self.user
        self.group.members.add(self.userProf)
        response = create_announcement(request, self.group.id)
        self.assertEqual(self.group.announcements.first().message, "test message")

    def test_create_then_remove_announcement(self):
        request = RequestFactory().post('/create_announcement/', {'message': "test message"})
        request.user = self.user
        self.group.members.add(self.userProf)
        create_announcement(request, self.group.id)
        announcement_id= self.group.announcements.first().id
        remove_announcement(request, self.group.id, announcement_id)
        self.assertEqual(self.group.announcements.all().count(), 0)


class CalendarTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        # make user1
        self.user = User.objects.create(username='Testuser')
        self.userProf = UserProfile(user=self.user, school='UVA', major='CS', state='VA', id=1,
                                    city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf.save()

        # make user2
        self.user2 = User.objects.create(username='Testuser2')
        self.userProf2 = UserProfile(user=self.user2, school='UVA', major='CS', state='VA', id=2,
                                     city='Charlottesville', discord_id='1234', zoom_id='1234567890', year=2)
        self.userProf2.save()
        # make group 1
        self.group = Group.objects.create(name="Group1", owner=self.userProf)

    def test_create_calendar (self):
        request = RequestFactory().post('/create_calendar/', {'monttt': True})
        request.user = self.user
        self.group.members.add(self.userProf)
        response = create_calendar(request, self.group.id)
        self.assertEqual(self.group.calendars.first().monttt, True)

    def test_create_then_remove_calendar(self):
        request = RequestFactory().post('/create_announcement/', {'monttt': True})
        request.user = self.user
        self.group.members.add(self.userProf)
        create_calendar(request, self.group.id)
        calendar_id= self.group.calendars.first().id
        remove_calendar(request, self.group.id, calendar_id)
        self.assertEqual(self.group.calendars.all().count(), 0)


class RedirectTests(TestCase):

    def test_user_list_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index/')

    def test_profile_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('self_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index/')

    def test_courses_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('uva_course_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index/')

    def test_create_group_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('create_group'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index/')

    def test_friends_list_when_not_logged_in(self):
        response = self.client.get(reverse('friends_list', args=[0]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index/')

    def test_create_calendar_when_not_logged_in(self):
        response = self.client.get(reverse('create_calendar', args=[0]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index/')

    def test_remove_calendar_when_not_logged_in(self):
        response = self.client.get(reverse('remove_calendar', args=[0, 0]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index/')