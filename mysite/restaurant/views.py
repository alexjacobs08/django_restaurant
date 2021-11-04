from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPosting, Restaurant, RestaurantLocation, Applicant
from django.forms import ModelForm
from rest_framework import generics
from .serializers import RestaurantSerializer, RestaurantLocationSerializer, JobPostingSerializer, ApplicantSerializer
from django.core.mail import send_mail

# API


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantLocationList(generics.ListCreateAPIView):
    queryset = RestaurantLocation.objects.all()
    serializer_class = RestaurantLocationSerializer


class RestaurantLocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantLocation.objects.all()
    serializer_class = RestaurantLocationSerializer


class JobPostingList(generics.ListCreateAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer


class JobPostingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer


class ApplicantList(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer


class ApplicantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer


# Forms

class ApplicationForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ['first_name', 'last_name', 'email', 'resume']


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'restaurant_admin']


class NewLocationForm(ModelForm):
    class Meta:
        model = RestaurantLocation
        fields = ['location', 'hiring_manager']


class PostingForm(ModelForm):
    class Meta:
        model = JobPosting
        fields = ['position']


# Non-template actions

def hiring_manager_job_posting_reopen(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    job_posting.closed = False
    job_posting.save()
    return redirect('hiring_manager_restaurant_detail', pk=job_posting.restaurant_location.id)


def hiring_manager_job_posting_close(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    job_posting.closed = True
    job_posting.save()
    return redirect('hiring_manager_restaurant_detail', pk=job_posting.restaurant_location_id)


def restaurant_admin_job_posting_reopen(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    job_posting.closed = False
    job_posting.save()
    return redirect('restaurant_location_detail', pk=job_posting.restaurant_location.id)


def restaurant_admin_job_posting_close(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    job_posting.closed = True
    job_posting.save()
    return redirect('restaurant_location_detail', pk=job_posting.restaurant_location_id)


def index(request, template_name='index.html'):
    return render(request, template_name)


# Applicant views


def job_postings(request, template_name='applicants/job_postings.html', message=None):
    job_postings = JobPosting.objects.all()
    context = {'job_postings': job_postings, 'message': message}
    return render(request, template_name, context)


def application_create(request, pk, template_name='applicants/application_form.html'):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    form = ApplicationForm(request.POST or None)
    if form.is_valid():
        application = form.save(commit=False)
        application.job_posting_id = job_posting.id
        application.closed = False
        application.save()
        return redirect('job_postings')

    return render(request, template_name, context={'job_posting': job_posting, 'form': form})


# Hiring manager views


def application_create_manager(request, pk, template_name='hiring_managers/application_form.html'):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    form = ApplicationForm(request.POST or None)
    if form.is_valid():
        application = form.save(commit=False)
        application.job_posting_id = job_posting.id
        application.closed = False
        application.save()
        return redirect('restaurant_location_detail', pk=job_posting.restaurant_location.pk)

    return render(request, template_name, context={'job_posting': job_posting, 'form': form})


def applications_view(request, pk, template_name='hiring_managers/application_detail.html'):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    applications = Applicant.objects.filter(job_posting_id=job_posting.id, rejected=False)

    return render(request, template_name, context={'applications': applications, 'job_posting': job_posting})


def application_approve(request, pk, template_name='hiring_managers/application_approve.html'):
    applicant = get_object_or_404(Applicant, pk=pk)
    job_posting = get_object_or_404(JobPosting, pk=applicant.job_posting_id)
    if request.method == 'POST':
        send_mail(
            'Application Status',
            f'Congratulations {applicant}! Your applicant for {job_posting.position} has been approved!',
            'from@example.com',
            [applicant.email],
            fail_silently=False,
        )
        job_posting.closed = True
        job_posting.save()
        return redirect('hiring_manager_restaurant_detail', pk=job_posting.restaurant_location.id)
    return render(request, template_name, context={'job_posting': job_posting, 'applicant': applicant})


def application_reject(request, pk, template_name='hiring_managers/application_reject.html'):
    applicant = get_object_or_404(Applicant, pk=pk)
    job_posting = get_object_or_404(JobPosting, pk=applicant.job_posting_id)
    if request.method == 'POST':
        send_mail(
            'Application Status',
            f'Hello {applicant}. Unfortunately, your application for {job_posting.position} has been rejected.',
            'from@example.com',
            [applicant.email],
            fail_silently=False,
        )
        applicant.rejected = True
        applicant.save()
        return redirect('hiring_manager_restaurant_detail', pk=job_posting.restaurant_location.id)
    return render(request, template_name, context={'job_posting': job_posting, 'applicant': applicant})


def hiring_manager_restaurant_detail(request, pk,
                                     template_name='hiring_managers/hiring_manager_restaurant_detail.html'):
    restaurant_location = get_object_or_404(RestaurantLocation, pk=pk)
    all_job_postings = JobPosting.objects.filter(restaurant_location=pk)
    open_job_postings = all_job_postings.filter(closed=False)
    closed_job_postings = all_job_postings.filter(closed=True)
    for open_job_posting in open_job_postings:
        open_job_posting.application_count = Applicant.objects.filter(job_posting_id=open_job_posting.id,
                                                                      rejected=False).count()
    for open_job_posting in closed_job_postings:
        open_job_posting.application_count = Applicant.objects.filter(job_posting_id=open_job_posting.id,
                                                                      rejected=False).count()
    form = PostingForm(request.POST or None)
    if form.is_valid():
        job_posting_form = form.save(commit=False)
        job_posting_form.restaurant = restaurant_location
        job_posting_form.save()
        return redirect('restaurant_location_detail', pk=pk)

    return render(request, template_name, context={'restaurant': restaurant_location,
                                                   'open_job_postings': open_job_postings,
                                                   'closed_job_postings': closed_job_postings, 'form': form})


def hiring_manager_view(request, template_name='hiring_managers/hiring_manager_view.html'):
    return render(request, template_name, context={'restaurant_list': Restaurant.objects.all()})


def hiring_manager_location_list(request, pk, template_name='hiring_managers/hiring_manager_location_list.html'):
    name = get_object_or_404(Restaurant, pk=pk)
    locations = RestaurantLocation.objects.filter(restaurant=pk)
    return render(request, template_name,
                  context={'restaurant_locations_list': locations, 'name': name.name})


# Restaurant Admin Views


def restaurant_list(request, template_name='restaurant_admin/restaurant_list.html'):
    return render(request, template_name, context={'restaurant_list': Restaurant.objects.all()})


def job_posting_update(request, pk, template_name='restaurant_admin/job_posting_form.html'):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    restaurant_location = job_posting.restaurant_location
    form = PostingForm(request.POST or None, instance=job_posting)
    if form.is_valid():
        form.save()
        return redirect('restaurant_location_detail', pk=restaurant_location.pk)
    return render(request, template_name, context={'form': form})


def job_posting_delete(request, pk, template_name='restaurant_admin/job_posting_delete.html'):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    restaurant_location = job_posting.restaurant_location
    if request.method == 'POST':
        job_posting.delete()
        return redirect('restaurant_location_detail', pk=restaurant_location.pk)
    return render(request, template_name,
                  context={'job_posting': job_posting, 'restaurant_location': restaurant_location})


def restaurant_detail(request, pk, template_name='restaurant_admin/restaurant_detail.html'):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    locations = RestaurantLocation.objects.filter(restaurant=pk)
    form = NewLocationForm(request.POST or None)
    if form.is_valid():
        new_location_form = form.save(commit=False)
        new_location_form.restaurant = restaurant
        new_location_form.save()
        return redirect('restaurant_detail', pk=pk)

    return render(request, template_name, context={'restaurant': restaurant, 'locations': locations, 'form': form})


def restaurant_location_update(request, pk, template_name='restaurant_admin/restaurant_location_form.html'):
    location = get_object_or_404(RestaurantLocation, pk=pk)
    form = NewLocationForm(request.POST or None, instance=location)
    if form.is_valid():
        form.save()
        return redirect('restaurant_detail', pk=pk)
    return render(request, template_name, context={'location': location, 'form': form})


def restaurant_location_delete(request, pk, template_name='restaurant_admin/restaurant_location_delete.html'):
    location = get_object_or_404(RestaurantLocation, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('restaurant_detail', pk=pk)
    return render(request, template_name, context={'location': location})


def restaurant_location_detail(request, pk, template_name='restaurant_admin/restaurant_location_detail.html'):
    location = get_object_or_404(RestaurantLocation, pk=pk)
    restaurant = get_object_or_404(Restaurant, pk=location.restaurant.id)

    all_job_postings = JobPosting.objects.filter(restaurant_location=pk)
    open_job_postings = all_job_postings.filter(closed=False)
    closed_job_postings = all_job_postings.filter(closed=True)
    for open_job_posting in open_job_postings:
        open_job_posting.application_count = Applicant.objects.filter(job_posting_id=open_job_posting.id,
                                                                      rejected=False).count()
    for open_job_posting in closed_job_postings:
        open_job_posting.application_count = Applicant.objects.filter(job_posting_id=open_job_posting.id,
                                                                      rejected=False).count()
    form = PostingForm(request.POST or None)
    if form.is_valid():
        job_posting_form = form.save(commit=False)
        job_posting_form.restaurant_location = location
        job_posting_form.save()
        return redirect('restaurant_location_detail', pk=pk)

    return render(request, template_name, context={'restaurant': restaurant, 'location': location,
                                                   'open_job_postings': open_job_postings,
                                                   'closed_job_postings': closed_job_postings, 'form': form})


def restaurant_create(request, template_name='restaurant_admin/restaurant_form.html'):
    form = RestaurantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('restaurant_list')

    return render(request, template_name, context={'form': form})


def restaurant_update(request, pk, template_name='restaurant_admin/restaurant_form.html'):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    form = RestaurantForm(request.POST or None, instance=restaurant)
    if form.is_valid():
        form.save()
        return redirect('restaurant_list')
    return render(request, template_name, context={'form': form})


def restaurant_delete(request, pk, template_name='restaurant_admin/restaurant_delete.html'):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurant_list')
    return render(request, template_name, context={'restaurant': restaurant})
