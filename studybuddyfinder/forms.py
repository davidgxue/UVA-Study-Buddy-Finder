from django.forms import forms, ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class CreateUserProfileForm(ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    class Meta:
        model = UserProfile
        fields = ('school','hide_school', 'major','hide_major', 'state', 'city', 'hide_state', 'year','hide_year','discord_id','zoom_id','bio')
        labels = {
            "hide_state": "Hide Location",
        }
 

# form for editing a user's profile
class EditUserProfileForm(ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    class Meta:
        model = UserProfile
        # include fields for school, major, state, year, discord/zoom ids, as well as the ability to hide them all
        fields = ('school', 'hide_school', 'major', 'hide_major', 'state', 'city', 'hide_state', 'year', 'hide_year', 'discord_id', 'zoom_id', 'bio')
        labels = {
            "hide_state": "Hide Location",
        }
# form for checking boxes to restrict a user list search
class SearchForm(forms.Form):
    empty_choices = [('','')]
    empty_choices.extend(list(UserProfile.school_choices))
    schools = tuple(empty_choices)
    restrict_school = forms.ChoiceField(required=False, label="School",  choices= schools)
    empty_choices = [('', '')]
    empty_choices.extend(list(UserProfile.year_choices))
    years = tuple(empty_choices)
    restrict_year = forms.ChoiceField(required=False, label="Year", choices= years)
    empty_choices = [('', '')]
    empty_choices.extend(list(UserProfile.major_choices))
    majors = tuple(empty_choices)
    restrict_major = forms.ChoiceField(required=False, label="Major", choices= majors)
    class_subject = forms.CharField(required=False, label="Course Designation", widget=forms.TextInput(attrs={'style': 'width:160px'}))
    class_number = forms.CharField(required=False, label="Course Number")
    class_name = forms.CharField(required=False, label="Course Title")



class ClassForm(forms.Form):
    class_subject = forms.CharField(required=False, label="Course Designation", widget=forms.TextInput(attrs={'style': 'width:160px'}))
    class_number = forms.CharField(required=False, label="Course Number")
    class_name = forms.CharField(required=False, label="Course Title")