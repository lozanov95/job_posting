from django.contrib.auth.decorators import login_required
from django.urls import path

from jobPosting.job_apply.views import SubmitApplicationView, ListMyApplicationsView, ListApplicantsView

urlpatterns = (
    path('apply/<int:pk>', login_required(SubmitApplicationView.as_view()), name='job apply'),
    path('my_applications/', login_required(ListMyApplicationsView.as_view()), name='my applications list'),
    path('applicants/<int:pk>', login_required(ListApplicantsView.as_view()), name='applications list'),

)
