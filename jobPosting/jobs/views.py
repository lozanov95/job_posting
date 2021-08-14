from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from jobPosting.jobs.models import JobPosting

UserModel = get_user_model()


def index(request):
    """
    Displaying the index page.
    Shows the last 5 job postings.
    """
    jobs = JobPosting.objects.all().order_by('-posted_on')[:5]
    context = {
        'object_list': jobs,
    }
    return render(request, 'index.html', context)


class CreateJobPostingView(CreateView):
    """
    Creating a new job posting.
    """
    model = JobPosting
    fields = ['title', 'category', 'description', 'city']
    template_name = 'jobs/create_job.html'
    success_url = reverse_lazy('job list')

    def form_valid(self, form):
        """
        Setting the current user as the one that posted the job.
        """
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class ListJobPostingsView(ListView):
    """
    Displays all job postings.
    """
    model = JobPosting
    template_name = 'jobs/list_jobs.html'
    extra_context = {'heading': 'Job postings:'}

    def get_queryset(self):
        """
        Ordering by time_posted in descending order
        """
        return JobPosting.objects.all().order_by('-posted_on')


class DetailsJobPostingView(DetailView):
    """
    Showing the details of a job posting
    """
    model = JobPosting
    template_name = 'jobs/jobs_details.html'


class EditJobPostingView(UpdateView):
    """
    View for editing a job posting.
    """
    model = JobPosting
    fields = ['title', 'category', 'description', 'city']
    template_name = 'jobs/job_update.html'
    success_url = reverse_lazy('index')


class DeleteJobPostingView(DeleteView):
    """
    Deletes a job posting
    """
    model = JobPosting
    template_name = 'jobs/confirm_delete.html'
    success_url = reverse_lazy('job list')

    def delete(self, request, *args, **kwargs):
        """
        Checking if the user doing the request is the original poster.
        If True - Deletes the posting
        If False - Returning error view
        """
        posting = JobPosting.objects.get(pk=kwargs.get('pk'))
        if request.user == posting.posted_by:
            return super().delete(request, *args, **kwargs)
        context = {
            'error_text': 'You are not authorized to perform this action'
        }
        return render(request, 'shared/error.html', context)


class MyJobsView(ListView):
    """
    Showing the job postings the current user
    """
    model = JobPosting
    template_name = 'jobs/list_jobs.html'
    extra_context = {'heading': 'My job postings:'}

    def get_queryset(self):
        queryset = JobPosting.objects.filter(posted_by=self.request.user).order_by('-posted_on')
        return queryset


def success_view(request):
    return render(request, 'shared/success.html')
