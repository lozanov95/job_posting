from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobPosting.jobs.urls')),
    path('auth/', include('jobPosting.job_auth.urls')),
    path('profile/', include('jobPosting.profiles.urls')),
]
