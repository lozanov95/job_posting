from django import forms

from jobPosting.jobs.models import JobPosting


class CreateJobPostingForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.Select(attrs={'class': 'form-select'})
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = JobPosting
        fields = ['title', 'category', 'description', 'city']
