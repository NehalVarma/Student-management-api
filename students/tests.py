from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Student


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            age=22,
            course="Computer Science"
        )

    def test_student_creation(self):
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.email, "john@example.com")
        self.assertEqual(str(self.student), "John Doe - Computer Science")


class StudentAPITest(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            age=25,
            course="Mathematics"
        )
        self.student_data = {
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "age": 20,
            "course": "Physics"
        }

    def test_get_student_list(self):
        url = reverse('student_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_create_student(self):
        url = reverse('student_list')
        response = self.client.post(url, self.student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_get_student_detail(self):
        url = reverse('student_detail', args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], self.student.name)

    def test_update_student(self):
        url = reverse('student_detail', args=[self.student.id])
        updated_data = {
            "name": "Jane Updated",
            "email": "jane.updated@example.com",
            "age": 26,
            "course": "Advanced Mathematics"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "Jane Updated")

    def test_delete_student(self):
        url = reverse('student_detail', args=[self.student.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)