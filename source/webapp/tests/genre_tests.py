from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse

from webapp.models import Genre


class GenreTest(TestCase):
    def setUp(self) -> None:
        self.init_users()
        self.genre = Genre.objects.create(title='Комедия')
        self.create_url = reverse('webapp:genre_create')
        self.update_url = reverse('webapp:genre_update', kwargs={'pk': self.genre.pk})
        self.delete_url = reverse('webapp:genre_delete', kwargs={'pk': self.genre.pk})

    def init_users(self):
        self.admin = User.objects.create_superuser(username='admin', password='admin', email='')
        self.redactor = User.objects.create(username='redactor', password='redactor')
        create_permission = Permission.objects.get(name='Can add genre')
        update_permission = Permission.objects.get(name='Can change genre')
        self.redactor.user_permissions.add(create_permission)
        self.redactor.user_permissions.add(update_permission)
        self.regular_user = User.objects.create(username='regular', password='regular')
        self.admin.set_password('admin')
        self.admin.save()
        self.redactor.set_password('redactor')
        self.redactor.save()
        self.regular_user.set_password('regular')
        self.regular_user.save()

    def test_create_permissions(self):
        response = self.client.get(self.create_url)
        self.assertEqual(reverse('accounts:login')+ '?next=' + self.create_url, response.url)

        self.client.login(username=self.admin.username, password = 'admin')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.redactor.username, password='redactor')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username = self.regular_user, password = 'regular')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 403)

    def test_change_permissions(self):

        response = self.client.get(self.update_url)
        self.assertEqual(reverse('accounts:login') + '?next=' + self.update_url, response.url)

        self.client.login(username=self.admin.username, password = 'admin')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.redactor.username, password='redactor')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username = self.regular_user, password = 'regular')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 403)

    def test_delete_permissions(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(reverse('accounts:login') + '?next=' + self.delete_url, response.url)

        self.client.login(username=self.admin.username, password='admin')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.redactor.username, password='redactor')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.regular_user, password='regular')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)

    def test_empty_create_request(self):
        self.client.login(username=self.redactor, password='redactor')
        response = self.client.post(self.create_url)
        self.assertFormError(response, form='form', field = 'title', errors='This field is required.')

    def test_empty_update_request(self):
        self.client.login(username=self.redactor, password='redactor')
        response = self.client.post(self.update_url)
        self.assertFormError(response, form='form', field = 'title', errors='This field is required.')

    def test_successfully_created(self):
        self.client.login(username=self.redactor, password='redactor')
        response = self.client.post(path=self.create_url, data={
            'title': 'Боевик',
        }, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(Genre.objects.filter(title='Боевик'))

    def test_successfully_updated(self):
        self.client.login(username=self.redactor, password = 'redactor')
        response = self.client.post(path=self.update_url, data={
            'title': 'Комедийные фильмы'
        }, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(self.genre.title, 'Комедийные фильмы')

    def test_successfully_deleted(self):
        self.client.login(username=self.admin.username, password='admin')
        response = self.client.post(self.delete_url)
        self.assertTrue(response.status_code, 200)
        self.assertFalse(Genre.objects.filter(title='Комедия'))



