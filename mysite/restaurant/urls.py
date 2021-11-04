from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('applicants/job_postings/', views.job_postings, name='job_postings'),
    path('applicants/apply/<int:pk>', views.application_create, name='application_create'),
    path('hiring_managers/', views.hiring_manager_view, name='hiring_manager_view'),
    path('hiring_managers/locations/<int:pk>', views.hiring_manager_location_list, name='hiring_manager_location_list'),
    path('hiring_managers/restaurant_detail/<int:pk>', views.hiring_manager_restaurant_detail, name='hiring_manager_restaurant_detail'),
    path('hiring_managers/posting_reopen/<int:pk>', views.hiring_manager_job_posting_reopen, name='hiring_manager_job_posting_reopen'),
    path('hiring_managers/posting_close/<int:pk>', views.hiring_manager_job_posting_close, name='hiring_manager_job_posting_close'),
    path('hiring_managers/applications/<int:pk>', views.applications_view, name='applications_view'),
    path('hiring_managers/application_approve/<int:pk>', views.application_approve, name='application_approve'),
    path('hiring_managers/application_reject/<int:pk>', views.application_reject, name='application_reject'),
    path('restaurant_list/', views.restaurant_list, name='restaurant_list'),
    path('restaurant_admin/view_location/<int:pk>', views.restaurant_location_detail, name='restaurant_location_detail'),
    path('restaurant_admin/view_location/application/<int:pk>', views.application_create_manager, name='application_create_manager'),
    path('restaurant_admin/restaurant/<int:pk>', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant_admin/update_location/<int:pk>', views.restaurant_location_update, name='restaurant_location_update'),
    path('restaurant_admin/delete_location/<int:pk>', views.restaurant_location_delete, name='restaurant_location_delete'),
    path('restaurant_admin/edit/<int:pk>', views.restaurant_update, name='restaurant_edit'),
    path('restaurant_admin/delete/<int:pk>', views.restaurant_delete, name='restaurant_delete'),
    path('restaurant_admin/new_restaurant/', views.restaurant_create, name='restaurant_new'),
    path('restaurant_admin/posting_reopen/<int:pk>', views.restaurant_admin_job_posting_reopen, name='restaurant_admin_job_posting_reopen'),
    path('restaurant_admin/posting_close/<int:pk>', views.restaurant_admin_job_posting_close, name='restaurant_admin_job_posting_close'),
    path('restaurant_admin/posting_update/<int:pk>', views.job_posting_update, name='job_posting_update'),
    path('restaurant_admin/posting_delete/<int:pk>', views.job_posting_delete, name='job_posting_delete'),
    path('api/restaurant/', views.RestaurantList.as_view(), name='restaurant-list'),
    path('api/restaurant/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant-detail'),
    path('api/restaurant_location/', views.RestaurantLocationList.as_view(), name='restaurantlocation-list'),
    path('api/restaurant_location/<int:pk>/', views.RestaurantLocationDetail.as_view(), name='restaurantlocation-detail'),
    path('api/job_posting/', views.JobPostingList.as_view(), name='jobposting-list'),
    path('api/job_posting/<int:pk>/', views.JobPostingDetail.as_view(), name='jobposting-detail'),
    path('api/applicant/', views.ApplicantList.as_view(), name='applicant-list'),
    path('api/applicant/<int:pk>/', views.ApplicantDetail.as_view(), name='applicant-detail'),

]

