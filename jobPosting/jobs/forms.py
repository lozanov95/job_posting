from django import forms

from jobPosting.jobs.models import Applicant


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['cv']
