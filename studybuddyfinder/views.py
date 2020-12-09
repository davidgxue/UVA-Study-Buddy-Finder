from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django import forms
from .forms import CreateUserProfileForm, EditUserProfileForm, SearchForm, ClassForm
from django.contrib.auth.models import User
from .models import UserProfile, FriendRequest, Group, Announcement, Course, Calendar
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect



def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('friends_list', kwargs={'is_creating_group':0}))
    else:
        return render(request, 'studybuddyfinder/index.html')
        

def login(request):
    if request.user.is_authenticated and not UserProfile.objects.filter(user_id=request.user.id).exists():
        return HttpResponseRedirect(reverse('register'))
    #return render(request, 'studybuddyfinder/index.html')
    return HttpResponseRedirect(reverse('friends_list', kwargs={'is_creating_group':0}))


def register(request):
    #if user is already registered, deny entry and redirect to index
    if request.user.is_authenticated and UserProfile.objects.filter(user_id=request.user.id).exists():
        return HttpResponseRedirect(reverse('friends_list', kwargs={'is_creating_group':0}))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        form = CreateUserProfileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            newusername= request.POST['username']
            if User.objects.filter(username=newusername).exists():
                raise forms.ValidationError(u'Username "%s" is not available.' % newusername)

            request.user.username = newusername
            request.user.save()

            profile=form.save(commit=False)
            profile.user= request.user

            #if the user email ends in .edu or .org, set student verified status
            #if request.user.email[-10:] == ".edu" or request.user.email[-4:] == "virginia.edu" :
            if request.user.email[-12:] == "virginia.edu":
                profile.student_verified = True
                
            
            profile.save()
            
            
            
            added_courses = profile.uva_courses.all()
            
            #unfiltered
            courses= Course.objects.all()

            context = {
                'list_of_all_courses': courses,
                'added_courses': added_courses,
                'alert_flag': True
            }
           # return HttpResponse("<html><body><p>Thanks for registering.</p><a href=\"/index\">Return to the homepage.</a></body></html>")
            #return render(request, 'studybuddyfinder/uva_course_list.html', context)
            #return HttpResponseRedirect(reverse('uva_course_list', kwargs={'alert_flag': True}))
            return HttpResponseRedirect(reverse('uva_course_list'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateUserProfileForm()
    return render(request, 'studybuddyfinder/register.html', {'form': form})

# this view is for editing your profile information
def edit(request):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    # if the user has submitted account changes
    if request.method == "POST":
        # get the profile we're editing and the submitted changes
        edit_profile = request.user.userprofile
        form = EditUserProfileForm(request.POST)
        # if the form is valid and we have actual changes
        if form.is_valid():
            # apply them
            edit_profile.school = request.POST['school']
            edit_profile.hide_school = bool(request.POST.get('hide_school'))
            edit_profile.major = request.POST['major']
            edit_profile.hide_major = bool(request.POST.get('hide_major'))
            edit_profile.state = request.POST['state']
            edit_profile.hide_state = bool(request.POST.get('hide_state'))
            edit_profile.city = request.POST['city']
           # edit_profile.hide_state = bool(request.POST.get('hide_state'))
            edit_profile.year = request.POST['year']
            edit_profile.hide_year = bool(request.POST.get('hide_year'))
            edit_profile.discord_id = request.POST['discord_id']
            edit_profile.zoom_id = request.POST['zoom_id']
            edit_profile.bio = request.POST['bio']
            # and save the model
            edit_profile.save()
            # render a link to the home page and tell the user their account has been updated.
            return HttpResponseRedirect(reverse('self_profile'))
        else: # if our form wasn't valid tell the user and redirect them to homepage
            return HttpResponse("<html><body><p>There was an error and your account was not updated.</p><a href=\"/index\">Return to the homepage.</a></body></html>")
    # yes yes I know this dictionary is DISGUSTING. let me live
    return render(request, 'studybuddyfinder/edit_account.html', {'form': EditUserProfileForm(initial={'school' : request.user.userprofile.school, 'hide_school' : request.user.userprofile.hide_school, 'major' : request.user.userprofile.major, 'hide_major' : request.user.userprofile.hide_major, 'city' : request.user.userprofile.city, 'state' : request.user.userprofile.state, 'hide_state' : request.user.userprofile.hide_state, 'year' : request.user.userprofile.year, 'hide_year' : request.user.userprofile.hide_year, 'discord_id' : request.user.userprofile.discord_id, 'zoom_id' : request.user.userprofile.zoom_id, 'bio' : request.user.userprofile.bio})})

def user_list(request):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    # create a form to use for both POSTS and GETS, as well as lists to filter out results
    form = SearchForm()
    filtered_list = UserProfile.objects.exclude(user=request.user)

    # if we are processing a search
    if request.method == 'POST':
        # if the form is valid
        form = SearchForm(request.POST)
        if form.is_valid():

            # grab the things that that the user searched
            school = request.POST['restrict_school']
            year = request.POST['restrict_year']
            major = request.POST['restrict_major']
            class_subject = request.POST['class_subject']
            class_number = request.POST['class_number']
            class_name = request.POST['class_name']

            if not class_subject == '':
                filtered_list = filtered_list.filter(uva_courses__subject__icontains=class_subject).distinct()

            if not class_name == '':
                filtered_list = filtered_list.filter(uva_courses__course_name__icontains=class_name).distinct()

            if not class_number == '':
                filtered_list = filtered_list.filter(uva_courses__course_number__icontains=class_number).distinct()

            # if the user searched for a school
            if not school == '':
                # filter out users without matching school and who have have hidden school
                filtered_list = filtered_list.filter(hide_school=False, school__icontains=school)

            # if the user searched for a year
            if not year == '':
                # filter out users without matching year and who have have hidden year
                filtered_list = filtered_list.filter(hide_year=False, year__icontains=year)

            # if the user searched for a major
            if not major == '':
                # filter out users without matching major and who have have hidden major
                filtered_list = filtered_list.filter(hide_major=False, major__icontains=major)

    # render the user_list template
    return render(request, 'studybuddyfinder/user_list.html', {'list_of_all_users': filtered_list, 'form': form, 'friends': get_friends_list(request)})

def get_friends_list(request):
    
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    # create an empty array to store the friend ids
    friend_ids = []
    # if the current user is valid
    if request.user.id:
        # get their user profile, their friend list, and all pending friend requests theyve sent
        profile = UserProfile.objects.get(user_id=request.user.id)
        all_friends= UserProfile.objects.get(user_id=request.user.id).friends.all()

        sent= FriendRequest.objects.filter(from_user=profile).all()
        received= FriendRequest.objects.filter(to_user=profile).all()
        for friend in received.iterator():
            friend_ids.append(friend.from_user.user.id)
        # go through each friend and add their id
        for friend in all_friends.iterator():
            friend_ids.append(friend.user.id)
        # go through each friend and add their id to sent
        for friend in sent.iterator():
            friend_ids.append(friend.to_user.user.id)
    
    return friend_ids

def send_request(request, id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    from_user = UserProfile.objects.get(user_id=request.user.id)
    try:
        to_user = UserProfile.objects.get(user_id=id)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect(reverse('user_list'))

    friend_request = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    return HttpResponseRedirect(reverse('user_list'))

def send_request_profile(request, id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    from_user= UserProfile.objects.get(user_id=request.user.id)
    try :
        to_user=UserProfile.objects.get(user_id=id)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[to_user]))

    friend_request= FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    return HttpResponseRedirect(reverse('profile', args=[to_user]))

def accept_request(request, friend_request_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    friend_request = FriendRequest.objects.get(id=friend_request_id)
    self = UserProfile.objects.get(user_id=request.user.id)
    sender = friend_request.from_user
    self.friends.add(sender)
    sender.friends.add(self)
    self.save()
    sender.save()
    friend_request.delete()
    return HttpResponseRedirect(reverse('friends_list', kwargs={'is_creating_group':0}))


def delete_request(request, friend_request_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.delete()
    return HttpResponseRedirect(reverse('friends_list', kwargs={'is_creating_group':0}))


def delete_friend(request, id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    profile = UserProfile.objects.get(user_id=request.user.id)
    friend_profile = UserProfile.objects.get(id=id)
    profile.friends.remove(friend_profile)  # A removes B
    friend_profile.friends.remove(profile)  # B removes A
    return HttpResponseRedirect(reverse('friends_list', kwargs={'is_creating_group':0}))


def friends_list(request, is_creating_group):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    friends = ""
    pending = ""
    sent = ""
    owned_groups = ""
    groups=""

    if request.user.id:
        profile = UserProfile.objects.get(user_id=request.user.id)
        friends = profile.friends.all()
        pending = FriendRequest.objects.filter(to_user=profile).all()
        sent = FriendRequest.objects.filter(from_user=profile).all()
        owned_groups = Group.objects.filter(owner=profile).all()
        groups= Group.objects.filter(members=profile).all()
    context = {
        'list_of_all_friends': friends,
        'pending': pending,
        'sent': sent,
        'groups': groups,
        'owned_groups': owned_groups,
        'is_creating_group': is_creating_group,
    }
    return render(request, 'studybuddyfinder/friends_list.html', context)


def logout_view(request):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    logout(request)
    return redirect('/index/')

# view to display a profile
def profile(request, username=""):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    #initialize variable for later use
    in_friend_list = False;

    # if we are displaying the user, make username their username
    if username == "":
        username = request.user.username
        user_profile = UserProfile.objects.get(user_id=request.user.id)
        courses = user_profile.uva_courses.all()

    # find the profile matching the username and store it
    profile = None;
    for user in User.objects.all():
        if user.username == username:
            profile = user
            user_profile = UserProfile.objects.get(user=profile)
            courses = user_profile.uva_courses.all()

    # if there was no matching user, raise an error
    if not profile:
        return HttpResponse("<html><body>There is no user with the username \"" + username + ".\"<p><a href=\"/index\">Return to the homepage.</a></p></body></html>")

    # if the user is being displayed, don't display an add friend button
    has_friend = request.user.username == profile.username;
    is_self = has_friend

    # if we haven't already decided not to display add friend button
    if not has_friend:
        # check to see if the user is already friends with them
        has_friend = UserProfile.objects.get(user_id=request.user.id).friends.filter(user_id=profile.id).exists()
        in_friend_list = UserProfile.objects.get(user_id=request.user.id).friends.filter(user_id=profile.id).exists()
        #Must use .exists for queryset, in does not work.
        #bugged not working: has_friend = profile in request.user.userprofile.friends.all()
        #bugged not working: in_friend_list = profile in request.user.userprofile.friends.all()

    # if we haven't already decided nto to display add friend button
    if not has_friend:
        # check to see if the user has a pending friend request either way
        for friend_request in list(FriendRequest.objects.all()):
            if (request.user.userprofile == friend_request.from_user and profile.userprofile == friend_request.to_user) or (request.user.userprofile == friend_request.to_user and profile.userprofile == friend_request.from_user):
                has_friend = True

    # package up information and display the profile view
    return render(request, 'studybuddyfinder/profile_view.html', {'user' : profile, 'show_friend_request' : not has_friend, 'show_edit' : is_self, 'in_friend_list': in_friend_list,'courses':courses})

def create_group(request):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    group_name = request.POST['group_name']
    profile = UserProfile.objects.get(user_id=request.user.id)
    Group.objects.get_or_create(name=group_name, owner=profile)
    return HttpResponseRedirect(reverse('friends_list', kwargs={'is_creating_group': 0}))


# Either the owner can remove a member or a member can remove themselves from the group
def remove_group_member(request, group_id, member_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    group = Group.objects.get(id=group_id)
    member = UserProfile.objects.get(id=member_id)
    group.members.remove(member)
    return HttpResponseRedirect(reverse('group_view', kwargs={'group_id': group_id}))


# assuming groups are not public, only group owner can add member
def add_group_member(request, group_id, member_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    group = Group.objects.get(id=group_id)
    member=UserProfile.objects.get(id=member_id)
    group.members.add(member)
    group.save()
    return HttpResponseRedirect(reverse('group_view', kwargs={'group_id': group_id}))

def group_view(request, group_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    try:
        name =''
        members =''
        owner =''
        friends = ''
        annoucements= ''
        calendars = ''
        memberusers = []
        can_post_avail = True

        if Group.objects.get(id=group_id):
            group = Group.objects.get(id=group_id)
            name = group.name
            owner = group.owner
            members = group.members.all()
            profile = UserProfile.objects.get(user_id=request.user.id)
            friends = profile.friends.all()
            announcements = list(group.announcements.all())
            calendars = list(group.calendars.all())
            
            #Anti-URL-Hopping: if user is not in group, redirect
            for m in members:
                memberusers.append(m.user)
            memberusers.append(owner.user)
            if not request.user in memberusers:
                return HttpResponseRedirect(reverse('index'))
            
                
            if calendars:
                for avail in calendars:
                    if avail.scheduler.user == request.user:
                        can_post_avail = False



        context = {
            'name': name,
            'owner': owner,
            'members': members,
            'friends': friends,
            'group_id': group_id,
            'announcements': announcements,
            'calendars' : calendars,
            'can_post_avail': can_post_avail
        }
        return render(request, 'studybuddyfinder/group_view.html', context)

    except:
        raise Http404('Group Not Found')

def create_announcement(request,group_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    profile = UserProfile.objects.get(user_id=request.user.id)
    poster = profile
    message = request.POST['message']
    group = Group.objects.get(id=group_id)
    announcement = Announcement.objects.get_or_create(poster=poster, message=message)
    group.announcements.add(announcement[0])
    group.save()
    return HttpResponseRedirect(reverse('group_view', kwargs={'group_id': group_id}))


def remove_announcement(request, group_id, announcement_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    announcement = Announcement.objects.get(id=announcement_id)
    group = Group.objects.get(id=group_id)

    if announcement.poster.user == request.user or group.owner== request.user:
        announcement.delete()

    return HttpResponseRedirect(reverse('group_view', kwargs={'group_id': group_id}))

def add_uva_course(request,course_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    profile = UserProfile.objects.get(user_id=request.user.id)
    course= Course.objects.get(id = course_id)
    profile.uva_courses.add(course)
    profile.save()
    return HttpResponseRedirect(reverse('uva_course_list'))

def remove_uva_course(request,course_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    profile = UserProfile.objects.get(user_id=request.user.id)
    course = Course.objects.get(id=course_id)
    profile.uva_courses.remove(course)
    return HttpResponseRedirect(reverse('self_profile'))

def uva_course_list(request):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    courses = ''
    added_courses = ''

    profile = UserProfile.objects.get(user_id=request.user.id)
    added_courses = profile.uva_courses.all()
    #print(added_courses)
    #unfiltered
    courses = Course.objects.all()

    form = ClassForm()

    if request.method == "POST":
        form = ClassForm(request.POST)
        
        if form.is_valid():
            class_subject = request.POST['class_subject']
            class_number = request.POST['class_number']
            class_title = request.POST['class_name']

            print(class_subject)

            courses = courses.filter(subject__icontains=class_subject.lower().strip())
            courses = courses.filter(course_number__icontains=class_number.lower().strip())
            courses = courses.filter(course_name__icontains=class_title.lower().strip())

    context = {
        'list_of_all_courses': courses,
        'added_courses': added_courses,
        'form': form,
    }
    return render(request, 'studybuddyfinder/uva_course_list.html', context)

#new stuff
def create_calendar(request,group_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    profile = UserProfile.objects.get(user_id=request.user.id)
    scheduler = profile
    #message = request.POST['message']
    group = Group.objects.get(id=group_id)
    '''
    mon = bool(request.POST.get('mon'))
    tues = bool(request.POST.get('tues'))
    wed = bool(request.POST.get('wed'))
    thurs = bool(request.POST.get('thurs'))
    fri = bool(request.POST.get('fri'))
    sat = bool(request.POST.get('sat'))
    sun = bool(request.POST.get('sun'))
    '''
    monttt = bool(request.POST.get('monttt'))
    montttwo = bool(request.POST.get('montttwo'))
    monttf = bool(request.POST.get('monttf'))
    monfts = bool(request.POST.get('monfts'))
    monste = bool(request.POST.get('monste'))

    tuesttt = bool(request.POST.get('tuesttt'))
    tuestttwo = bool(request.POST.get('tuestttwo'))
    tuesttf = bool(request.POST.get('tuesttf'))
    tuesfts = bool(request.POST.get('tuesfts'))
    tuesste = bool(request.POST.get('tuesste'))

    wedttt = bool(request.POST.get('wedttt'))
    wedtttwo = bool(request.POST.get('wedtttwo'))
    wedttf = bool(request.POST.get('wedttf'))
    wedfts = bool(request.POST.get('wedfts'))
    wedste = bool(request.POST.get('wedste'))

    thursttt = bool(request.POST.get('thursttt'))
    thurstttwo = bool(request.POST.get('thurstttwo'))
    thursttf = bool(request.POST.get('thursttf'))
    thursfts = bool(request.POST.get('thursfts'))
    thursste = bool(request.POST.get('thursste'))

    frittt = bool(request.POST.get('frittt'))
    fritttwo = bool(request.POST.get('fritttwo'))
    frittf = bool(request.POST.get('frittf'))
    frifts = bool(request.POST.get('frifts'))
    friste = bool(request.POST.get('friste'))

    satttt = bool(request.POST.get('satttt'))
    sattttwo = bool(request.POST.get('sattttwo'))
    satttf = bool(request.POST.get('satttf'))
    satfts = bool(request.POST.get('satfts'))
    satste = bool(request.POST.get('satste'))

    sunttt = bool(request.POST.get('sunttt'))
    suntttwo = bool(request.POST.get('suntttwo'))
    sunttf = bool(request.POST.get('sunttf'))
    sunfts = bool(request.POST.get('sunfts'))
    sunste = bool(request.POST.get('sunste'))

    calendar = Calendar.objects.get_or_create(scheduler=scheduler, monttt=monttt, montttwo=montttwo, monttf=monttf, monfts=monfts, monste=monste,
    tuesttt=tuesttt, tuestttwo=tuestttwo, tuesttf=tuesttf, tuesfts=tuesfts, tuesste=tuesste,
    wedttt=wedttt, wedtttwo=wedtttwo, wedttf=wedttf, wedfts=wedfts, wedste=wedste,
    thursttt=thursttt, thurstttwo=thurstttwo, thursttf=thursttf, thursfts=thursfts, thursste=thursste,
    frittt=frittt, fritttwo=fritttwo, frittf=frittf, frifts=frifts, friste=friste,
    satttt=satttt, sattttwo=sattttwo, satttf=satttf, satfts=satfts, satste=satste,
    sunttt=sunttt, suntttwo=suntttwo, sunttf=sunttf, sunfts=sunfts, sunste=sunste)
    group.calendars.add(calendar[0])
    group.save()
    return HttpResponseRedirect(reverse('group_view', kwargs={'group_id': group_id}))

def remove_calendar(request, group_id, calendar_id):
    # if the user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    calendar = Calendar.objects.get(id=calendar_id)
    group = Group.objects.get(id=group_id)

    if calendar.scheduler.user == request.user or group.owner.user == request.user:
        calendar.delete()

    return HttpResponseRedirect(reverse('group_view', kwargs={'group_id': group_id}))
