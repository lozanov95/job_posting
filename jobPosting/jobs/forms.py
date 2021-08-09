from django import forms
from django.contrib.auth import get_user_model

from jobPosting.jobs.models import JobPosting

UserModel = get_user_model()


class JobPostingCreateForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'category', 'description', 'posted_by']
        widgets = {'posted_by': forms.HiddenInput()}

