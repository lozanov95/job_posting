from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from jobPosting.jobs.views import ListJobPostingsView, DetailsJobPostingView, \
    CreateJobPostingView, DeleteJobPostingView, index

urlpatterns = (
    path('', index, name='index'),
    path('list/', ListJobPostingsView.as_view(), name='job list'),
    path('create/', login_required(CreateJobPostingView.as_view(), reverse_lazy('job list')), name='job create'),
    path('details/<int:pk>', DetailsJobPostingView.as_view(), name='job details'),
    path('delete/<int:pk>', DeleteJobPostingView.as_view(), name='job delete'),
)
