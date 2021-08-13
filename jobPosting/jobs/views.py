from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from jobPosting.jobs.models import JobPosting, Applicant

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
        queryset = JobPosting.objects.filter(posted_by=self.request.user)
        return queryset


class SubmitApplicationView(CreateView):
    model = Applicant
    template_name = 'jobs/apply.html'
    fields = ['cv']
    success_url = reverse_lazy('success')

    def get(self, request, *args, **kwargs):
        """
        Overriding get, so I could pass the pk on the get request
        """
        self.request.pk = kwargs.get('pk')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Matching the user and the job posting.
        Returns error view in the following cases:
            - User have already applied
            - User is the job poster
            - The file extension is not in the allowed extensions list
        """
        allowed_extensions = ['pdf', 'docx']
        context = {
            "error_text": [],
        }
        file_ext = form.instance.cv.name.split('.')[-1]
        job = JobPosting.objects.get(pk=self.kwargs['pk'])
        application = Applicant.objects.filter(applicant=self.request.user, job_application=job)

        if application:
            context['error_text'].append('You have already applied for this job.')
        if self.request.user == job.posted_by:
            context['error_text'].append('You cannot apply for a job that you have submitted.')
        if file_ext not in allowed_extensions:
            context['error_text'].append(
                f'This extension is not supported! You must use only the following extensions {", ".join(allowed_extensions)}.')
        if len(context['error_text']) > 0:
            return render(self.request, 'shared/error.html', context)

        form.instance.job_application = job
        form.instance.applicant = self.request.user
        return super().form_valid(form)


def success_view(request):
    return render(request, 'shared/success.html')


class ListMyApplicationsView(ListView):
    """
    Showing the applications of the current user
    """
    model = Applicant
    template_name = 'jobs/list_jobs.html'
    extra_context = {'heading': 'My applications'}

    def get_queryset(self):
        """
        Filtering the queryset, so only the results of the current user are shown
        """
        applications = Applicant.objects.filter(applicant=self.request.user).select_related('job_application') \
            .order_by('-applied_on')
        jobs = [job.job_application for job in applications]
        return jobs


class ListApplicantsView(ListView):
    """
    Displaying list of applicants for the job posting.
    """
    model = Applicant
    template_name = 'jobs/applicants_list.html'

    def get_queryset(self):
        queryset = Applicant.objects.filter(job_application__id=self.kwargs.get('pk')).select_related('applicant')
        return queryset
