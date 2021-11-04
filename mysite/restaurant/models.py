from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    restaurant_admin = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class RestaurantLocation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    hiring_manager = models.CharField(max_length=30)


class JobPosting(models.Model):
    restaurant_location = models.ForeignKey(RestaurantLocation, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    date_posted = models.DateField(auto_now_add=True)
    closed = models.BooleanField(default=False)


class Applicant(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    date_applied = models.DateField(auto_now_add=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    email = models.EmailField()
    resume = models.TextField(blank=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
