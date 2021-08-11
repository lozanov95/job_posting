from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from jobPosting.jobs.views import ListJobPostingsView, DetailsJobPostingView, \
    CreateJobPostingView, DeleteJobPostingView, index, EditJobPostingView, MyJobsView, \
    SubmitApplicationView, success_view, ListMyApplicationsView, ListApplicantsView

urlpatterns = (
    path('', index, name='index'),
    path('list/', ListJobPostingsView.as_view(), name='job list'),
    path('my_jobs/', MyJobsView.as_view(), name='job my postings'),

    path('create/', login_required(CreateJobPostingView.as_view()), name='job create'),
    path('details/<int:pk>', DetailsJobPostingView.as_view(), name='job details'),
    path('update/<int:pk>', login_required(EditJobPostingView.as_view()), name='job edit'),
    path('delete/<int:pk>', login_required(DeleteJobPostingView.as_view()), name='job delete'),

    path('apply/<int:pk>', login_required(SubmitApplicationView.as_view()), name='job apply'),
    path('my_aplications/', login_required(ListMyApplicationsView.as_view()), name='my applications list'),
    path('applicants/<int:pk>', login_required(ListApplicantsView.as_view()), name='applications list'),

    path('success/', success_view, name='success'),
)
