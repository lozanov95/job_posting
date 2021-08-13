from django import forms

from jobPosting.profiles.models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form used for displaying/editing the profile information.
    """

    class Meta:
        model = Profile
        exclude = ('user', 'is_complete')
