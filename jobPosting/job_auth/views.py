from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from jobPosting.job_auth.forms import SignInForm, SignUpForm


def sign_up(request):
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign in')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'auth/sign-up.html', context)


def sign_in(request):
    if request.POST:
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignInForm()

    context = {
        'form': form,
    }

    return render(request, 'auth/sign-in.html', context)


@login_required
def sign_out(request):
    logout(request)
    return redirect('index')
