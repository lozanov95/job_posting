from django.test import TestCase, Client
from jobPosting.jobs.models import JobCategory, JobPosting


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
        JobCategory(name=category_name).save()

        self.create_endpoint = '/create/'
        self.job_object = {'title': 'test name', 'category': 1, 'description': 'test description',
                           'city': 'test city'}

        self.c = Client()
        self.c.post('/auth/sign-up/', {'email': email, 'password1': pwd, 'password2': pwd})
        self.c.post('/auth/sign-in/', {'email': email, 'password': pwd})

    def test_create_posting(self):
        self.c.post(self.create_endpoint, self.job_object)
        self.assertEqual(len(JobPosting.objects.filter(title=self.job_object.get('title'))), 1)

    def test_details_post(self):
        self.c.post(self.create_endpoint, self.job_object)
        response = self.c.get('/details/1')
        self.assertContains(response, self.job_object['title'])

    def test_edit_post(self):
        new_object = self.job_object
        new_object['title'] = 'edited title'
        self.c.post(self.create_endpoint, self.job_object)
        self.c.post('/update/1', new_object)
        self.assertEqual(len(JobPosting.objects.filter(title=new_object['title'])), 1)

    def test_delete_post(self):
        self.c.post(self.create_endpoint, self.job_object)
        self.assertEqual(len(JobPosting.objects.filter(title=self.job_object['title'])), 1,
                         'The object was not created')
        self.c.post('/delete/1')
        self.assertEqual(len(JobPosting.objects.filter(title=self.job_object['title'])), 0,
                         'The object was not deleted')

    def test_my_jobs(self):
        self.c.post(self.create_endpoint, self.job_object)
        response = self.c.get('/my_jobs/')
        self.assertContains(response, self.job_object['title'])

    def test_job_list(self):
        self.c.post(self.create_endpoint, self.job_object)
        response = self.c.get('/list/')
        self.assertContains(response, self.job_object['title'])
