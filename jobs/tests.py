from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Job


class JobTests(APITestCase):
    # In Python, the @classmethod decorator is used to declare a method in the class as a class method that can be called using ClassName.MethodName()
    # click the blue circle, this overrides a particular method
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_job = Job.objects.create(
            name="rake",
            owner=testuser1,
            description="Better for collecting leaves than a shovel.",
        )
        test_job.save()

    # NEW
    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_jobs_model(self):
        job = Job.objects.get(id=1)
        actual_owner = str(job.owner)
        actual_name = str(job.name)
        actual_description = str(job.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "rake")
        self.assertEqual(
            actual_description, "Better for collecting leaves than a shovel."
        )

    def test_get_job_list(self):
        url = reverse("job_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jobs = response.data
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["name"], "rake")

    def test_get_job_by_id(self):
        url = reverse("job_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job = response.data
        self.assertEqual(job["name"], "rake")

    def test_create_job(self):
        url = reverse("job_list")
        data = {"owner": 1, "name": "spoon", "description": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        jobs = Job.objects.all()
        self.assertEqual(len(jobs), 2)
        self.assertEqual(Job.objects.get(id=2).name, "spoon")

    def test_update_job(self):
        url = reverse("job_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "rake",
            "description": "pole with a crossbar toothed like a comb.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job = Job.objects.get(id=1)
        self.assertEqual(job.name, data["name"])
        self.assertEqual(job.owner.id, data["owner"])
        self.assertEqual(job.description, data["description"])

    def test_delete_job(self):
        url = reverse("job_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        jobs = Job.objects.all()
        self.assertEqual(len(jobs), 0)

    # New
    def test_authentication_required(self):
        self.client.logout()
        url = reverse("job_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
