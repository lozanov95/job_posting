from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from jobPosting.jobs.views import ListJobPostingsView, DetailsJobPostingView, \
    CreateJobPostingView, DeleteJobPostingView, index, EditJobPostingView, MyJobsView

urlpatterns = (
    path('', index, name='index'),
    path('list/', ListJobPostingsView.as_view(), name='job list'),
    path('my_jobs', MyJobsView.as_view(), name='job my postings'),
    path('create/', login_required(CreateJobPostingView.as_view(), reverse_lazy('sign in')), name='job create'),
    path('details/<int:pk>', DetailsJobPostingView.as_view(), name='job details'),
    path('update/<int:pk>', EditJobPostingView.as_view(), name='job edit'),
    path('delete/<int:pk>', DeleteJobPostingView.as_view(), name='job delete'),
)
