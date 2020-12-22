import os
import unittest

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from members.models import Member, StudyProgram
from members.forms import CustomUserCreationForm
from rest_framework.test import APITestCase
from rest_framework import status


class MemberCheckAPITest(APITestCase):
    def test_person_is_not_member(self):
        """
        Test if a person is not a member of UTN
        """
        url = reverse('member_check_api')
        data = {'ssn': '196001010101'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('is_member'), False)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_person_is_member(self):
        """
        Test if a person is a member of UTN
        """
        url = reverse('member_check_api')
        data = {'ssn': '199105050203'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('is_member'), True)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_invalid_ssn(self):
        """
        Test if a person with an invalid ssn causes an ERROR
        """
        url = reverse('member_check_api')
        data = {'ssn': '0000'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("error" in response.data)
        self.assertEqual(response['Content-Type'], 'application/json')


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
        self.member = Member.objects.create_user(
            username='moore',
            password='Intel1968',
            email='g.moore@localhost',
            phone_number="0733221111",
            melos_id='123456789',
            study=self.study,
            registration_year='1946',
        )

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

    def test_change_study(self):
        new_study = StudyProgram.objects.create(
            name_en='Superhero',
            name_sv='Superhjälte',
            degree='msc',
        )
        data = {
            'study': new_study.id.__str__(),
            'registration_year': '1980',
            'email': self.member.email,
            'phone_number': self.member.phone_number
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
        self.assertEqual(formatted_phone, "073-322 11 11")

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
            'person_number': '199105050203',
            'email': 'g.moore@localhost',
            'phone_number': '0700000000',
            'password1': 'Test!234',
            'password2': 'Test!234',
        }
        response = self.client.post(reverse('register'), information)

        # Successful -> redirect to login.
        self.assertRedirects(response, reverse('login'))

        # A member has been created with the correct information
        member = Member.objects.get(username=information['username'])
        self.assertEqual(member.email, information['email'])
        self.assertEqual(member.phone_number, information['phone_number'])
        self.assertEqual(member.name, "Firstname Lastname")
        self.assertEqual(member.person_nr, information['person_number'])

        # Email has been sent to confirm e-mail address
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [information['email']])

        # You can login with the provided credentials
        self.assertTrue(self.client.login(
            username=information['username'],
            password=information['password1'],
        ))


class UserCreationFormTest(TestCase):
    def setUp(self):
        self.user = {
            'username': 'test_basic_creation',
            'person_number': '199105050203',
            'email': 'g.moore@localhost',
            'phone_number': '0700000000',
            'password1': 'Test!234',
            'password2': 'Test!234',
        }

    def test_creation(self):
        form = CustomUserCreationForm(data=self.user)
        self.assertTrue(form.is_valid())

        form.save()
        member = Member.objects.get(username=self.user['username'])

        self.assertEqual(member.username, self.user['username'])
        self.assertEqual(member.email, self.user['email'])
        self.assertEqual(member.phone_number, self.user['phone_number'])
        self.assertEqual(member.person_nr, self.user['person_number'])
        self.assertEqual(member.name, "Firstname Lastname")

    def test_create_superuser(self):
        self.user["is_superuser"] = True

        form = CustomUserCreationForm(data=self.user)
        self.assertTrue(form.is_valid())

        form.save()
        member = Member.objects.get(username=self.user['username'])
        self.assertTrue(member.is_superuser)
        self.assertTrue(member.is_staff)
