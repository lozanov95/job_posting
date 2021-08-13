from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from jobPosting.job_apply.models import Applicant
from jobPosting.jobs.models import JobPosting


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
