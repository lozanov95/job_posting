from django.contrib import admin

from jobPosting.jobs.models import JobCategory, JobPosting, Applicant

admin.site.register(JobCategory)
admin.site.register(JobPosting)
admin.site.register(Applicant)
