from django.urls import reverse
from rest_framework import status
from products.models import Category
from rest_framework.test import APITestCase
from custom_auth.types import User


class CategoryTest(APITestCase):
    # python manage.py dumpdata products.Category --format=yaml --indent=4 > products/fixtures/categories.yaml
    fixtures = ['categories']

    def setUp(self):
        self.user = User.objects.create_user(phone_number='+998903651422', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category_1 = Category.objects.first()

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_category_detail(self):
        url = reverse('category-detail', args=[self.category_1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create(self):
        url = reverse('category-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)

    def test_category_update(self):
        url = reverse('category-detail', args=[self.category_1.pk])
        data = {'name': 'Electronic Gadgets'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_delete(self):
        url = reverse('category-detail', args=[self.category_1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)