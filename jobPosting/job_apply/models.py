from django.contrib.auth import get_user_model
from django.db import models

from jobPosting.jobs.models import JobPosting

UserModel = get_user_model()


class Applicant(models.Model):
    """
    This model represents a single job application.
    """
    applicant = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )
    job_application = models.ForeignKey(
        to=JobPosting,
        on_delete=models.CASCADE,
    )
    cv = models.FileField(
        upload_to='applicant_cv',
    )
    applied_on = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.job_application} - {self.applicant}'
