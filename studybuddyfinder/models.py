from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):

    state_choices = (
        ('Virginia', 'Virginia'),
        ('Alabama', 'Alabama'),
        ('Alaska', 'Alaska'),
        ('American Samoa', 'American Samoa'),
        ('Arizona', 'Arizona'),
        ('Arkansas', 'Arkansas'),
        ('California', 'California'),
        ('Colorado', 'Colorado'),
        ('Connecticut', 'Connecticut'),
        ('Delaware', 'Delaware'),
        ('District of Colombia', 'District of Colombia'),
        ('Florida', 'Florida'),
        ('Georgia', 'Georgia'),
        ('Guam', 'Guam'),
        ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'),
        ('Indiana', 'Indiana'),
        ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'),
        ('Kentucky', 'Kentucky'),
        ('Louisiana', 'Louisiana'),
        ('Maine', 'Maine'),
        ('Maryland', 'Maryland'),
        ('Massachussets', 'Massachussets'),
        ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'),
        ('Mississippi', 'Mississippi'),
        ('Missouri', 'Missouri'),
        ('Montana', 'Montana'),
        ('Nebraska', 'Nebraska'),
        ('Nevada', 'Nevada'),
        ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'),
        ('New Mexico', 'New Mexico'),
        ('New York', 'New York'),
        ('North Carolina', 'North Carolina'),
        ('North Dakota', 'North Dakota'),
        ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'),
        ('Oregon', 'Oregon'),
        ('Pennsylvania', 'Pennsylvania'),
        ('Puerto Rico', 'Puerto Rico'),
        ('Rhode Island', 'Rhode Island'),
        ('South Carolina', 'South Carolina'),
        ('South Dakota', 'South Dakota'),
        ('Tennesse', 'Tennessee'),
        ('Texas', 'Texas'),
        ('US Virgin Islands', 'US Virgin Islands'),
        ('Utah', 'Utah'),
        ('Vermont', 'Vermont'),
        ('Washington', 'Washington'),
        ('West Virginia', 'West Virginia'),
        ('Wisconsin', 'Wisconsin'),
        ('Wyoming', 'Wyoming'),
    )

    major_choices = (
        ('Aerospace Engineering', 'Aerospace Engineering'),
        ('African American and African Studies', 'African American and African Studies'),
        ('Anthropology', 'Anthropology'),
        ('Archaeology', 'Archaeology'),
        ('Arichtectural History', 'Arichtectural History'),
        ('Architecture', 'Architecture'),
        ('Astronomy', 'Astronomy'),
        ('Biology', 'Biology'),
        ('Biomedical Engineering', 'Biomedical Engineering'),
        ('Chemical Engineering', 'Chemical Engineering'),
        ('Chemistry', 'Chemistry'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Classics', 'Classics'),
        ('Cognitive Science', 'Cognitive Science'),
        ('Commerce', 'Commerce'),
        ('Comparative Literature', 'Comparative Literature'),
        ('Computer Engineering', 'Computer Engineering'),
        ('Computer Science', 'Computer Science'),
        ('Dance', 'Dance'),
        ('Drama', 'Drama'),
        ('East Asian Languages', 'East Asian Languages'),
        ('Economics', 'Economics'),
        ('Electical Engineering', 'Electrical Engineering'),
        ('English', 'English'),
        ('Environmental Sciences', 'Environmental Science'),
        ('French', 'French'),
        ('German', 'German'),
        ('German Studies', 'German Studies'),
        ('Global Studies', 'Global Studies'),
        ('History', 'History'),
        ('History of Art', 'History of Art'),
        ('Human Biology', 'Human Biology'),
        ('Jewish Studies', 'Jewish Studies'),
        ('Kinesiology', 'Kinesiology'),
        ('Latin American Studies', 'Latin American Studies'),
        ('Linguistics', 'Linguistics'),
        ('Materials Science and Engineering', 'Materials Science and Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Media Studies', 'Media Studies'),
        ('South Asian Languages', 'South Asian Languages'),
        ('Music', 'Music'),
        ('Neuroscience', 'Neuroscience'),
        ('Nursing', 'Nursing'),
        ('Philosophy', 'Philosophy'),
        ('Physics', 'Physics'),
        ('Political and Social Thought', 'Political and Social Thought'),
        ('Politics', 'Politics'),
        ('Psychology', 'Psychology'),
        ('Religious Studies', 'Religious Studies'),
        ('Slavic Languages and Literature', 'Slavic Languages and Literature'),
        ('Sociology', 'Sociology'),
        ('Spanish', 'Spanish'),
        ('Statistics', 'Statistics'),
        ('Studio Art', 'Studio Art'),
        ('Systems Engineering', 'Systems Engineering'),
        ('Urban and Environmental Planning', 'Urban and Environmental Planning'),
        ('Women, Gender, and Sexuality', 'Women, Gender, and Sexuality'),
    )

    school_choices = (
        ('College of Arts & Sciences', 'College of Arts & Sciences'),
        ('School of Engineering and Applied Science', 'School of Engineering and Applied Science'),
        ('McIntire School of Commerce', 'McIntire School of Commerce'),
        ('Frank Batten School of Leadership and Public Policy', 'Frank Batten School of Leadership and Public Policy'),
        ('School of Architecture', 'School of Architecture'),
        ('School of Data Science', 'School of Data Science'),
        ('Darden School of Business', 'Darden School of Business'),
        ('School of Law', 'School of Law'),
        ('School of Medicine', 'School of Medicine'),
        ('Graduate School of Arts & Sciences', 'Graduate School of Arts & Sciences'),
        ('School of Nursing', 'School of Nursing'),
        ('School of Continuing & Professional Studies', 'School of Continuing & Professional Studies'),
        ('School of Education and Human Development', 'School of Education and Human Development'),        
    )

    year_choices = (
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year'),
        ('Graduate Student', 'Graduate Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, choices=school_choices)
    hide_school = models.BooleanField(default=False, blank=False)
    major = models.CharField(max_length=100,null=True, choices=major_choices)
    hide_major = models.BooleanField(default=False, blank=False)
    state = models.CharField(max_length=100,null=True, choices=state_choices)
    hide_state = models.BooleanField(default=False, blank=False)
    city = models.CharField(max_length=100,null=True)
    discord_id = models.CharField(max_length=100,null=True)
    zoom_id = models.CharField(max_length=100,null=True)
    year = models.CharField(max_length=100, choices=year_choices)
    hide_year = models.BooleanField(default=False, blank=False)
    student_verified= models.BooleanField(default=False)
    friends = models.ManyToManyField('UserProfile', blank=True)
    uva_courses= models.ManyToManyField('Course', blank=True)
    bio= models.CharField(max_length=10000, blank=True)
    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name="to_user", on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(UserProfile, related_name="owner", on_delete=models.CASCADE)
    members = models.ManyToManyField('UserProfile', blank=True)
    announcements = models.ManyToManyField('Announcement', blank=True)
    #adding field here
    calendars = models.ManyToManyField('Calendar', blank=True)
    def __str__(self):
        return "{}'s Group". format(self.owner)


class Announcement(models.Model):
    poster = models.ForeignKey(UserProfile, related_name="poster", on_delete=models.CASCADE)
    message = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField("Date", auto_now_add=True,null=True)


class Course(models.Model):
    course_name= models.CharField(max_length=100, null=True)
    subject= models.CharField(max_length=100, null=True)
    course_number= models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.course_name

class Calendar(models.Model):
    scheduler = models.ForeignKey(UserProfile, related_name="scheduler", on_delete=models.CASCADE)

    monttt = models.BooleanField(default=False, blank=False)
    montttwo = models.BooleanField(default=False, blank=False)
    monttf = models.BooleanField(default=False, blank=False)
    monfts = models.BooleanField(default=False, blank=False)
    monste = models.BooleanField(default=False, blank=False)

    tuesttt = models.BooleanField(default=False, blank=False)
    tuestttwo = models.BooleanField(default=False, blank=False)
    tuesttf = models.BooleanField(default=False, blank=False)
    tuesfts = models.BooleanField(default=False, blank=False)
    tuesste = models.BooleanField(default=False, blank=False)

    wedttt = models.BooleanField(default=False, blank=False)
    wedtttwo = models.BooleanField(default=False, blank=False)
    wedttf = models.BooleanField(default=False, blank=False)
    wedfts = models.BooleanField(default=False, blank=False)
    wedste = models.BooleanField(default=False, blank=False)

    thursttt = models.BooleanField(default=False, blank=False)
    thurstttwo = models.BooleanField(default=False, blank=False)
    thursttf = models.BooleanField(default=False, blank=False)
    thursfts = models.BooleanField(default=False, blank=False)
    thursste = models.BooleanField(default=False, blank=False)

    frittt = models.BooleanField(default=False, blank=False)
    fritttwo = models.BooleanField(default=False, blank=False)
    frittf = models.BooleanField(default=False, blank=False)
    frifts = models.BooleanField(default=False, blank=False)
    friste = models.BooleanField(default=False, blank=False)

    satttt = models.BooleanField(default=False, blank=False)
    sattttwo = models.BooleanField(default=False, blank=False)
    satttf = models.BooleanField(default=False, blank=False)
    satfts = models.BooleanField(default=False, blank=False)
    satste = models.BooleanField(default=False, blank=False)

    sunttt = models.BooleanField(default=False, blank=False)
    suntttwo = models.BooleanField(default=False, blank=False)
    sunttf = models.BooleanField(default=False, blank=False)
    sunfts = models.BooleanField(default=False, blank=False)
    sunste = models.BooleanField(default=False, blank=False)
    #mon = models.BooleanField(default=False, blank=False)
    #tues = models.BooleanField(default=False, blank=False)
    #wed = models.BooleanField(default=False, blank=False)
    #thurs = models.BooleanField(default=False, blank=False)
    #fri = models.BooleanField(default=False, blank=False)
    #sat = models.BooleanField(default=False, blank=False)
    #sun = models.BooleanField(default=False, blank=False)