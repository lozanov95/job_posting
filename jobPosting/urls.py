from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('jobPosting.jobs.urls')),
                  path('auth/', include('jobPosting.job_auth.urls')),
                  path('profile/', include('jobPosting.profiles.urls')),
                  path('apply/', include('jobPosting.job_apply.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
