from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class JobCategory(models.Model):
    name = models.CharField(
        max_length=20,
    )

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    title = models.CharField(
        max_length=30,
    )
    category = models.ForeignKey(
        to=JobCategory,
        on_delete=models.CASCADE,
    )
    description = models.TextField()
    city = models.CharField(
        max_length=15,
        null=False,
        blank=False,
    )
    posted_by = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    posted_on = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated_on = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.category} - {self.title}"


class Applicant(models.Model):
    applicant = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )
    job_application = models.ForeignKey(
        to=JobPosting,
        on_delete=models.CASCADE,
    )
    cv = models.FileField(
        upload_to='media'
    )

    def __str__(self):
        return f'{self.job_application} - {self.applicant}'
