from django import forms

from jobPosting.profiles.models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form used for displaying/editing the profile information.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        exclude = ('user', 'is_complete')
