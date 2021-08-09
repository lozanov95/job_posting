from django.contrib import admin

from jobPosting.jobs.models import JobCategory, JobPosting

admin.site.register(JobCategory)
admin.site.register(JobPosting)
