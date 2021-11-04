from .models import JobPosting, Restaurant, RestaurantLocation, Applicant
from rest_framework import serializers


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'restaurant_admin']


class RestaurantLocationSerializer(serializers.HyperlinkedModelSerializer):
    restaurant = serializers.HyperlinkedRelatedField(read_only=True,
                                                     view_name='restaurant-detail')

    class Meta:
        model = RestaurantLocation
        fields = ['url', 'restaurant', 'location', 'hiring_manager']


class JobPostingSerializer(serializers.HyperlinkedModelSerializer):
    restaurant_location = serializers.HyperlinkedRelatedField(read_only=True,
                                                              view_name='restaurantlocation-detail')

    class Meta:
        model = JobPosting
        fields = ['url', 'restaurant_location', 'position', 'date_posted', 'closed']


class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    job_posting = serializers.HyperlinkedRelatedField(read_only=True, view_name='jobposting-detail')

    class Meta:
        model = Applicant
        fields = ['url', 'job_posting', 'date_applied', 'last_name', 'first_name', 'email', 'resume', 'rejected']
