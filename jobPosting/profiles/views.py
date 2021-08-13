from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from jobPosting.profiles.forms import ProfileForm
from jobPosting.profiles.models import Profile


@login_required
def profile_details(request):
    """
    Displays the user's profile information.
    Enables the user to edit their profile information.
    """
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }

    return render(request, 'profiles/details.html', context)
