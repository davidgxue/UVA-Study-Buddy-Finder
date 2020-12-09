# project-2-02
CS 3240 Project-2-02 UVA Study Buddy Finder




<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/uva-cs3240-f20/project-2-02">
    <img src="studybuddyfinder/static/icon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">UVA CS 3240 Project: UVA Study Buddy Finder</h3>

  <p align="center">
    Project created for CS 3240 by Team Sherriff's Deputies (see developers below)
    <br />
    <br />
    <a href="https://studdy-buddy-finder.herokuapp.com/">View Demo Website</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [How does it work](#how-does-it-work)
  * [Registration](#registration)
  * [My Study Buddies Dashboard](#my-study-buddies-dashboard)
  * [Study Group Page](#study-group-page)
  * [Find a Study Buddy Page](#find-a-study-buddy-page)
  * [User Profile Page](#user-profile-page)
  * [Edit Account Page](#edit-account-page)
  * [References](#References)
* [Developers](#developers)




<!-- ABOUT THE PROJECT -->
## About The Project
**Overview**

The UVA Study Buddy Finder is a website, specifically a web app, designed to assist UVA students to find study peers according to their need. It allows users to set up their account with their interests, course schedule, what they need help with, as well as other information related to finding study peers, and it generates study buddies and study groups dynamically based upon similar learning needs and interests.

![Product Name Screen Shot][product-screenshot]

### How does it work
The Study Buddy Finder works by prompting users to sign up with a Google email account, and create an account with our system by typing their year, major, and other personal information, as well as a bio about their study habits and what they would like to improve on. After they have finished registering, users can click on the "Find A Buddy" page, where they can search for other users using search filters such as year, major, and courses and send friend requests to other users. Then, users can go to the "My Study Buddies" page to view and accept friend requests, as well as create study groups. When a user is part of a Study Group, they can add the times they are available to study and if they are the owner of a group, make announcements about upcoming meeting times. More information about each section of the Study Buddy Finder can be found below.  

### Registration
To register for an account, simply click on the "Signup/Login" button in the center of the website or use the button at the top right corner of the main page. Then, choose the Google account the user desire to login with. Although UVA Google Account is not required, UVA students are encouraged to use their UVA account for better user experience. When prompted with the create a profile form, enter all information on the page including username, school, major, hometown city and state, year, Discord ID, Zoom ID and a Bio. The user can also choose to hide some information from other users if they have privacy concerns.

If the registration is successful, the user is redirected to the UVA courses page where the user can search the courses they are taking or need help with and add them to their profile.

### My Study Buddies Dashboard
"My Study Buddies" page is the main dashboard of the website for users who are logged in. This page contains various information including friend list, incoming and outoging friend requests, study groups owned, and study groups where the user is a member of. The user can perform various actions on this page such as accept friend requests, remove friends and create study groups. 

### Study Group Page
Each study group is associated with a study group page. On this page, members of the group can check out other group members, post and view availability times, see recent announcements made by the group owner or leave the group. Each user can only make one availability post at a time, and they must remove their existing post to post a new one. Owners of the group can manage the group through removing group members, adding group members from friend list and posting announcements to the group. The owner can also remove availability posts of other users.

### Find a Study Buddy Page
The "Find a Study Buddy" page can entered through the top navigation bar of the website. This page allows the user to search for study buddies based on their preferences. The users can search for a study buddy using various filters including school, year, major, course desgination, course number and course title. Multiple filters can be applied at the same time but only one filter is needed for the search. When users chose to hide some particular information such as major, the user will not be displayed on the search results using this specific filter. Each user's profile page can then be accessed after the search, and the user can choose to add them as friends if they desire.


### User Profile Page
Each user has their own user profile page which contains all their information as well as UVA courses that can be accessed by clicking the "My Account" option on the top right corner of the website. Users can also access other users' user profiles by clicking on their usernames anytime. However, the user profile page may display different information depending on different factors. Users who are not friends with each other can only see their publicly displayed information with their Discord and Zoom ID hidden. Likewise, users who are friends with each other can see each others' information including the Discord and Zoom ID with the exception of the information they chose to hide.

### Edit Account Page
The user can edit their account information through the edit account page. This page can be accessed by clicking the "My Account" option on the top right corner, and click the "Edit" button to edit their information. Through this page, the UVA courses page can also be accessed and the user can choose to add or remove courses to their schedule.


### References
Libraries and APIs:
* []()Bootstrap
  * []() Title: Bootstrap
  * []() Author: https://github.com/orgs/twbs/people
  * []() Date: 11/20/2020
  * []() Code version: 4.5
  * []() URL: https://getbootstrap.com/docs/4.5/about/license/
  * []() Software License: MIT License
* []()Django Framework
  * []() Title: Django
  * []() Author: https://www.djangoproject.com/foundation/
  * []() Date: 11/20/2020
  * []() Code version: 3.1.3
  * []() URL: https://github.com/django/django/blob/master/LICENSE
  * []() Software License: BSD-3
* []()Django-allauth
  * []() Title: django-allauth
  * []() Author: Raymond Penners
  * []() Date: 11/20/2020
  * []() Code version: 0.43.0
  * []() URL: https://pypi.org/project/django-allauth/
  * []() Software License: MIT
* []()Django-Bootstrap4
  * []() Title: Django-Bootstrap4
  * []() Author: Dylan Verheul
  * []() Date: 11/20/2020
  * []() Code version: 2.3.1
  * []() URL: https://pypi.org/project/django-bootstrap4/
  * []() Software License: BSD-3
* []()Laptop Workstation Office Work Image
  * []() Title: Laptop Workstation Office Work Image
  * []() Author: Peter Olexa https://pixabay.com/users/deeezy-15467098/
  * []() Date: 11/20/2020
  * []() URL: https://pixabay.com/photos/laptop-workstaion-office-work-4906312/
  * []() Software License: Pixabay License (https://pixabay.com/service/license/)
* []()UVA Dev Hub API (Linked Externally, not directly used)
  * []() Title: UVA Dev Hub API
  * []() Author: University of Virginia
  * []() Date: 11/20/2020
  * []() Code version: N/A
  * []() URL: https://devhub.virginia.edu/index
  * []() Software License: Free Personal Copy - No License






<!-- CONTACT -->
## Developers
* []()Kayla Lewis - ksl3fs@virgnia.edu
* []()David Xue - dx8zp@virginia.edu
* []()Kevin Mulliss - kam8ef@virginia.edu
* []()Sindhu Mente - snm6dhh@virginia.edu


Project Link: [https://github.com/uva-cs3240-f20/project-2-02](https://github.com/uva-cs3240-f20/project-2-02)





<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: Screenshot1.PNG
