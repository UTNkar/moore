import os
import unittest

from django.core import mail
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.test import TestCase
import datetime

from django.urls import reverse

from members import cron
from members.forms import PersonNumberField
from members.models import Member, StudyProgram


class MemberTest(TestCase):
    """
    Unit tests for the Member Model
    """

    def setUp(self):
        self.member = Member.objects.create(username='moore')
        self.assertEqual(1, Member.objects.count())

    def test_print_person_number(self):
        self.member.birthday = datetime.date(1929, 1, 3)
        self.member.person_number_ext = '1234'
        self.assertEqual(
            '19290103-1234', self.member.person_number(),
            'Person numbers are printed as \'(year)(month)(day)-(ext)\'.'
        )

    def test_empty_person_number(self):
        self.assertEqual(
            '', self.member.person_number(),
            'A empty string is returned if no person number data is available'
        )

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
            first_name='Gordon',
            last_name='Moore',
            email='g.moore@localhost',
            birthday=datetime.date(1929, 1, 3),
            person_number_ext='1234',
            phone_number='+461234567890',
            registration_year='1946',
            study=self.study,
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
        self.assertContains(response, self.member.first_name,
                            msg_prefix='Response contains first name')
        self.assertContains(response, self.member.last_name,
                            msg_prefix='Response contains last name')
        self.assertContains(response, self.member.person_number(),
                            msg_prefix='Response contains person number')
        self.assertContains(response, self.member.phone_number,
                            msg_prefix='Response contains phone number')
        self.assertContains(response, self.member.email,
                            msg_prefix='Response contains email address')
        self.assertContains(response,
                            '<option value="'
                            + self.member.study_id.__str__()
                            + '" selected="selected">')
        self.assertContains(response, self.member.registration_year,
                            msg_prefix='Response contains registration year')

    def test_change_contact(self):
        data = {
            'first_name': 'Flash',
            'last_name': 'Gordon',
            'person_number': '19340107-9876',
            'phone_number': '+31612345678',

        }
        response = self.client.post(reverse('profile'), data)

        # No errors occurred in the change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {})

        # The contact information has been changed
        member = Member.objects.get(username='moore')
        self.assertEqual(member.first_name, data['first_name'])
        self.assertEqual(member.last_name, data['last_name'])
        self.assertEqual(
            member.birthday, datetime.date(1934, 1, 7)
        )
        self.assertEqual(member.person_number_ext, '9876')
        self.assertEqual(member.person_number(), data['person_number'])
        self.assertEqual(member.phone_number, data['phone_number'])

    def test_change_study(self):
        new_study = StudyProgram.objects.create(
            name_en='Superhero',
            name_sv='Superhjälte',
            degree='msc',
        )
        data = {
            'study': new_study.id.__str__(),
            'registration_year': '1980',
            # required fields
            'person_number': self.member.person_number(),
            'first_name': self.member.first_name,
            'last_name': self.member.last_name,
        }
        response = self.client.post(reverse('profile'), data)

        # No errors occurred in the change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {})

        # The contact information has been changed
        member = Member.objects.get(username='moore')
        self.assertEqual(member.study, new_study)
        self.assertEqual(member.registration_year, data['registration_year'])

    def test_change_email(self):
        new_email = 'f.gordon@localhost'
        data = {
            'email': 'f.gordon@localhost',
            # required fields
            'person_number': self.member.person_number(),
            'first_name': self.member.first_name,
            'last_name': self.member.last_name,
        }
        response = self.client.post(reverse('profile'), data)

        # No errors occurred in the change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {})

        # An unconfirmed email address has been added
        self.assertContains(
            response,
            'Your newly set email address has not yet been confirmed',
        )
        member = Member.objects.get(username='moore')
        self.assertIn(new_email, member.get_unconfirmed_emails())

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, [new_email])
        self.assertIn(
            self.member.get_confirmation_key(new_email), mail.outbox[1].body
        )


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
            username='moore',
            birthday=datetime.date(1929, 1, 3),
            person_number_ext='1234',
        )
        self.flash = Member.objects.create(
            username='flash',
            birthday=datetime.date(1934, 1, 7),
            person_number_ext='9876',
        )

    @unittest.skipIf(os.environ.get('TRAVIS', 'false') == 'true',
                     'Skipping this test on Travis CI.')
    def test_signal(self):
        self.assertEqual(self.moore.status, 'member')
        self.assertEqual(self.flash.status, 'nonmember')

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

    @unittest.skipIf(os.environ.get('TRAVIS', 'false') == 'true',
                     'Skipping this test on Travis CI.')
    def test_cron(self):
        Member.objects.filter(pk=self.moore.pk).update(status='unknown')
        Member.objects.filter(pk=self.flash.pk).update(status='unknown')

        cron.update_membership_status()
        self.moore.refresh_from_db()
        self.assertEqual(self.moore.status, 'member')
        self.flash.refresh_from_db()
        self.assertEqual(self.flash.status, 'nonmember')


class PersonNumberFieldTestCase(TestCase):
    def setUp(self):
        self.field = PersonNumberField()

    def test_blank(self):
        result = self.field.clean('')
        self.assertEqual(result, (None, ''))

    def test_pass(self):
        result = self.field.clean('19290103-1234')
        self.assertEqual(result, (datetime.date(1929, 1, 3), '1234'))

    def test_t_number(self):
        result = self.field.clean('19340107-T987')
        self.assertEqual(result, (datetime.date(1934, 1, 7), 'T987'))

    def test_non_date(self):
        with self.assertRaises(ValidationError):
            self.field.clean('00000000-1234')

    def test_incomplete(self):
        with self.assertRaises(ValidationError):
            self.field.clean('19290103-12')
        with self.assertRaises(ValidationError):
            self.field.clean('1929010-1234')

    def test_illegal_character(self):
        with self.assertRaises(ValidationError):
            self.field.clean('19290$03-1234')
        with self.assertRaises(ValidationError):
            self.field.clean('19290103-12t4')

    def test_widget_additions(self):
        widget = TextInput()
        attrs = self.field.widget_attrs(widget)
        self.assertIn('person_number', attrs['class'])
        self.assertEqual(attrs['placeholder'], 'YYYYMMDD-XXXX')
