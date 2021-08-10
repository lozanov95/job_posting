from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from jobPosting.jobs.models import JobPosting

UserModel = get_user_model()


def index(request):
    jobs = JobPosting.objects.all().order_by('-posted_on')[:5]
    context = {
        'jobs': jobs,
    }
    return render(request, 'index.html', context)


class CreateJobPostingView(CreateView):
    model = JobPosting
    fields = ['title', 'category', 'description', 'city']
    template_name = 'jobs/create_job.html'
    success_url = reverse_lazy('job list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class ListJobPostingsView(ListView):
    model = JobPosting
    template_name = 'jobs/list_jobs.html'
    extra_context = {'heading': 'Job postings:'}

    def get_queryset(self):
        return JobPosting.objects.all().order_by('-posted_on')


class DetailsJobPostingView(DetailView):
    model = JobPosting
    template_name = 'jobs/jobs_details.html'


class EditJobPostingView(UpdateView):
    model = JobPosting
    fields = ['title', 'category', 'description', 'city']
    template_name = 'jobs/job_update.html'
    success_url = reverse_lazy('index')


class DeleteJobPostingView(DeleteView):
    model = JobPosting
    template_name = 'jobs/confirm_delete.html'
    success_url = reverse_lazy('job list')

    def delete(self, request, *args, **kwargs):
        posting = JobPosting.objects.get(pk=kwargs.get('pk'))
        if request.user == posting.posted_by:
            return super().delete(request, *args, **kwargs)
        return HttpResponseForbidden('You are not authorized to perform this action!')


class MyJobsView(ListView):
    model = JobPosting
    template_name = 'jobs/list_jobs.html'
    extra_context = {'heading': 'My job postings:'}

    def get_queryset(self):
        queryset = JobPosting.objects.filter(posted_by=self.request.user)
        return queryset
