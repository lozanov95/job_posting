from django.urls import path
from jobPosting.profiles.views import profile_details
import jobPosting.profiles.signals

urlpatterns = (
    path('', profile_details, name='profile details'),
)
