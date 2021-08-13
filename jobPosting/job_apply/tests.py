from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse_lazy

from jobPosting.job_apply.models import Applicant
from jobPosting.jobs.models import JobPosting, JobCategory

UserModel = get_user_model()


class ApplicantTestCase(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        self.email_job_poster = 'job_poster@gmail.com'
        self.email_job_applicant = 'job_applicant@gmail.com'
        self.password = 'Qwerty1234!'

        self.user_poster = UserModel(email=self.email_job_poster)
        self.user_poster.set_password(self.password)
        self.user_poster.save()

        self.user_applicant = UserModel(email=self.email_job_applicant)
        self.user_applicant.set_password(self.password)
        self.user_applicant.save()

        JobCategory(name='test_cat').save()
        JobPosting(
            title='j title',
            description='j desc',
            city='j city',
            category=JobCategory.objects.first(),
            posted_by=self.user_poster,
        ).save()

        self.job = JobPosting.objects.first()

    def apply_job(self, email, file_name):
        self.c.post(reverse_lazy('sign in'), {'email': email, 'password': self.password})
        file = SimpleUploadedFile(file_name, b'content!')
        self.c.post(reverse_lazy('job apply', kwargs={'pk': self.job.id}), data={'cv': file})

    def test_job_apply(self):
        self.apply_job(self.user_applicant.email, 'great_file.pdf')
        self.assertTrue(Applicant.objects.filter(job_application=self.job).exists())
        self.assertEqual(Applicant.objects.filter(job_application=self.job).first().applicant, self.user_applicant)

    def test_job_apply_incorrect_file_ext(self):
        self.apply_job(self.user_applicant.email, 'great_file.cmd')
        self.assertFalse(Applicant.objects.filter(job_application=self.job).exists())

    def test_job_apply_to_self_job(self):
        self.apply_job(self.user_poster.email, 'great_file.pdf')
        self.assertFalse(Applicant.objects.filter(job_application=self.job).exists())

    def test_job_apply_twice(self):
        self.apply_job(self.user_applicant.email, 'great_file.pdf')
        self.apply_job(self.user_applicant.email, 'great_file.pdf')
        self.assertEqual(len(Applicant.objects.filter(job_application=self.job)), 1)

    def test_my_applications(self):
        self.apply_job(self.user_applicant.email, 'great_file.pdf')
        response = self.c.get(reverse_lazy('my applications list'))
        self.assertContains(response, self.job.title)
        self.assertContains(response, self.job.city)

    def test_applicants(self):
        self.apply_job(self.user_applicant.email, 'great_file.pdf')
        self.c.get(reverse_lazy('sign out'))
        self.c.post(reverse_lazy('sign in'), {'email': self.user_poster.email, 'password': self.password})
        response = self.c.get(reverse_lazy('applications list', kwargs={'pk': self.job.id}))
        self.assertContains(response, self.user_applicant.email)
