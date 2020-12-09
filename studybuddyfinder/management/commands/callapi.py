from django.core.management.base import BaseCommand, CommandError
import requests
from studybuddyfinder.models import Course
class Command(BaseCommand):

    def handle(self, *args, **options):
        url = 'https://api.devhub.virginia.edu/v1/courses'
        data = requests.get(url).json()
        Course.objects.all().delete()
        print("Number of Courses: "+str(len(data["class_schedules"]["records"])))
        courses= data["class_schedules"]["records"]

        filtered= [course for course in courses if course[12] == '2020 Fall']
        print("Number of Courses Fall 2020: "+ str(len(filtered)))

        def unique(a):
            found = []
            for value in a:
                if value[4] not in found:
                    yield value
                    found.append(value[4])

        no_duplicates= list(unique(filtered))
        print("Number of Courses Fall 2020 (only one section per course): "+str(len(no_duplicates)))
        for course in no_duplicates:
            Course.objects.get_or_create(course_name=course[4], subject= course[0] ,course_number= course[1])