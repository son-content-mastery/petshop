from django.test import SimpleTestCase
from django.urls import reverse


class ContactPageTests(SimpleTestCase):
    def test_contact_page_renders(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')

    def test_contact_submission_redirects_to_success_page(self):
        response = self.client.post(
            reverse('contact'),
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'phone': '0123456789',
                'message': 'Testing the contact flow.',
            },
        )

        self.assertRedirects(response, reverse('contact_success'))

    def test_contact_success_page_renders(self):
        response = self.client.get(reverse('contact_success'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/contact/success/')
