from django.contrib import admin
from .models import JobPosting, Restaurant, RestaurantLocation, Applicant

admin.site.register(JobPosting)
admin.site.register(Restaurant)
admin.site.register(RestaurantLocation)
admin.site.register(Applicant)
