from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

from jobPosting.jobs.models import JobCategory, JobPosting

UserModel = get_user_model()


class JobPostingTestCase(TestCase):
    """
    Testing the CRUD functionality of JobPosting
    """

    def setUp(self) -> None:
        """
        Configuring the commonly used vars
        """
        email = 'test@abv.bg'
        pwd = 'Qwerty1234!'
        category_name = 'IT - Software'

        self.c = Client()
        self.c.post(reverse_lazy('sign up'), {'email': email, 'password1': pwd, 'password2': pwd})
        self.c.post(reverse_lazy('sign in'), {'email': email, 'password': pwd})
        JobCategory(name=category_name).save()
        JobPosting(
            title='title 1',
            description='description 1',
            city='City 1',
            category=JobCategory.objects.first(),
            posted_by=UserModel.objects.first(),
        ).save()
        self.user = UserModel.objects.first()
        self.category = JobCategory.objects.first()

    def test_create_posting(self):
        job_title = 'title_new'
        self.c.post(reverse_lazy('job create'),
                    {'title': job_title, 'description': 'desc 2', 'city': 'c2',
                     'category': self.category.id})
        self.assertTrue(JobPosting.objects.filter(title=job_title).exists())

    def test_details_post(self):
        job = JobPosting.objects.first()
        response = self.c.get(reverse_lazy('job details', kwargs={'pk': job.id}))
        self.assertContains(response, job.title)

    def test_edit_post(self):
        job = JobPosting.objects.first()
        job.title = 'new_title'
        self.c.post(reverse_lazy('job edit', kwargs={'pk': job.id}),
                    {'title': job.title, 'description': job.description, 'city': job.city, 'category': job.category.id})
        self.assertTrue(JobPosting.objects.filter(title=job.title).exists())

    def test_delete_post(self):
        job = JobPosting.objects.first()
        self.c.post(reverse_lazy('job delete', kwargs={'pk': job.id}))
        self.assertFalse(JobPosting.objects.filter(pk=job.id).exists())

    def test_my_jobs(self):
        job_title = 'my jobs t'
        self.c.post(reverse_lazy('job create'),
                    {'title': job_title,
                     'description': 'my jobs d',
                     'city': 'my jobs c',
                     'category': self.category.id})
        response = self.c.get(reverse_lazy('job my postings'))
        self.assertContains(response, job_title)

    def test_job_list(self):
        job = JobPosting.objects.first()
        response = self.c.get(reverse_lazy('job list'))
        self.assertContains(response, job.title)
