import os
import unittest

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from members.models import Member, StudyProgram


class MemberTest(TestCase):
    """
    Unit tests for the Member Model
    """

    def setUp(self):
        self.member = Member.objects.create(username='moore')
        self.assertEqual(1, Member.objects.count())

    def test_study_deletion(self):
        study = StudyProgram.objects.create(name_en='subject')
        self.member.study = study
        self.member.save()
        study.delete()
        self.member.refresh_from_db()
        self.assertEqual(
            None, self.member.study,
            'Deleting a study program resets the study for the members'
        )


class ProfileTest(TestCase):
    """
    Tests for the profile page and subsequent form.
    """

    def setUp(self):
        # Create test objects
        self.study = StudyProgram.objects.create(
            name_en='Chemistry',
            name_sv='Kemi',
            degree='bsc',
        )
        self.member = Member.objects.create(
            username='moore',
            email='g.moore@localhost',
            registration_year='1946',
            study=self.study,
            phone_number='0733221131'
        )
        self.member.set_password('Intel1968')
        self.member.save()

        self.client.login(username='moore', password='Intel1968')

    def test_login_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
                         reverse('login') + '?next=' + reverse('profile'))

    def test_initial_data(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<option value="'
                            + self.member.study_id.__str__()
                            + '" selected>')
        self.assertContains(response, self.member.registration_year,
                            msg_prefix='Response contains registration year')

    def test_change_contact(self):
        data = {
            'first_name': 'Flash',
            'last_name': 'Gordon',
        }

        response = self.client.post(reverse('profile'), data, follow=True)

        # No errors occurred in the change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {})

    def test_change_study(self):
        new_study = StudyProgram.objects.create(
            name_en='Superhero',
            name_sv='Superhjälte',
            degree='msc',
        )
        data = {
            'study': new_study.id.__str__(),
            'registration_year': '1980',
        }
        response = self.client.post(reverse('profile'), data, follow=True)

        # No errors occurred in the change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {})

        # The contact information has been changed
        member = Member.objects.get(username='moore')
        self.assertEqual(member.study, new_study)
        self.assertEqual(member.registration_year, data['registration_year'])

    def test_phone_format(self):
        formatted_phone = self.member.get_phone_formatted
        self.assertEqual(formatted_phone, "073-322 11 31")

        self.member.phone_number = "+442083661177"

        formatted_phone = self.member.get_phone_formatted
        self.assertEqual(formatted_phone, "+44 20 8366 1177")


class EmailConfirmationTest(TestCase):
    """Tests for the sending of confirmations of new email addresses"""

    def setUp(self):
        # Create test objects
        self.member = Member.objects.create(
            username='moore',
            email='g.moore@localhost',
        )

    def test_send_on_creation(self):
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.member.email])
        self.assertIn(
            self.member.get_confirmation_key(), mail.outbox[0].body
        )

    def test_send_on_change(self):
        new_email = 'gordon@localhost'
        token = self.member.add_email_if_not_exists(new_email)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, [new_email])
        self.assertIn(
            token, mail.outbox[1].body
        )

    def test_confirm(self):
        self.member.set_password('Intel1968')
        self.member.save()
        self.client.login(username='moore', password='Intel1968')

        response = self.client.get(reverse('email_change_confirm', kwargs={
            'token': self.member.get_confirmation_key()
        }), follow=True)

        self.assertContains(
            response, 'Your email address has been confirmed.',
        )
        self.assertIn(self.member.email, self.member.get_confirmed_emails())

    def test_invalid_confirm(self):
        self.member.set_password('Intel1968')
        self.member.save()
        self.client.login(username='moore', password='Intel1968')

        response = self.client.get(reverse('email_change_confirm', kwargs={
            'token': 'trololololol'
        }), follow=True)

        self.assertContains(
            response, 'The provided confirmation token was invalid.',
        )
        self.assertNotIn(self.member.email, self.member.get_confirmed_emails())


class MembershipAPITest(TestCase):
    def setUp(self):
        self.moore = Member.objects.create(
            username='moore'
        )
        self.flash = Member.objects.create(
            username='flash'
        )

    @unittest.skipIf(os.environ.get('TRAVIS', 'false') == 'true',
                     'Skipping this test on Travis CI.')
    def test_signal(self):
        self.assertEqual(self.moore.status, 'member')
        self.assertEqual(self.flash.status, 'member')

    def test_method(self):
        self.moore.status = 'unknown'
        self.moore.update_status('member')
        self.assertEqual(self.moore.status, 'member')

        self.moore.status = 'unknown'
        self.moore.update_status('nonmember')
        self.assertEqual(self.moore.status, 'nonmember')

        self.moore.status = 'member'
        self.moore.update_status('member')
        self.assertEqual(self.moore.status, 'member')

        self.moore.status = 'member'
        self.moore.update_status('nonmember')
        self.assertEqual(self.moore.status, 'alumnus')

        self.moore.status = 'alumnus'
        self.moore.update_status('member')
        self.assertEqual(self.moore.status, 'member')

        self.moore.status = 'alumnus'
        self.moore.update_status('nonmember')
        self.assertEqual(self.moore.status, 'alumnus')

        self.moore.status = 'nonmember'
        self.moore.update_status('member')
        self.assertEqual(self.moore.status, 'member')

        self.moore.status = 'nonmember'
        self.moore.update_status('nonmember')
        self.assertEqual(self.moore.status, 'nonmember')


class RegistrationTestCase(TestCase):
    """
    Tests for the registration page
    """

    def test_basic_creation(self):
        information = {
            'username': 'test_basic_creation',
            'person_number': '199100000000',
            'email': 'g.moore@localhost',
            'phone_number': '070000000',
            'password1': 'Test!234',
            'password2': 'Test!234',
        }
        response = self.client.post(reverse('register'), information)

        # Successful -> redirect to login.
        self.assertRedirects(response, reverse('login'))

        # A member has been created with the correct information
        member = Member.objects.get(username=information['username'])
        self.assertEqual(member.email, information['email'])

        # Email has been sent to confirm e-mail address
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [information['email']])

        # You can login with the provided credentials
        self.assertTrue(self.client.login(
            username=information['username'],
            password=information['password1'],
        ))
