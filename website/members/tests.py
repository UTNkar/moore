from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime

from members.models import Member, StudyProgram


class MemberTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.member = Member.objects.create(user=self.user)
        self.assertEqual(1, Member.objects.count())

    def test_delete_cascade(self):
        self.user.delete()
        self.assertEqual(
            0, Member.objects.count(),
            'Deleting a user deletes the member information.'
        )

    def test_user_link(self):
        self.assertEqual(
            self.user, self.member.user,
            'Members are linked to a user object.'
        )

    def test_print_person_number(self):
        self.member.birthday = datetime.strptime('09/07/1999', '%d/%m/%Y')
        self.member.person_number_ext = '1234'
        self.assertEqual(
            '19990709-1234', self.member.person_number(),
            'Person numbers are printed as \'(year)(month)(day)-(ext)\'.'
        )

    def test_study_deletion(self):
        study = StudyProgram.objects.create(name='subject')
        self.member.study = study
        self.member.save()
        study.delete()
        self.member.refresh_from_db()
        self.assertEqual(
            None, self.member.study,
            'Deleting a study program resets the study for the members'
        )
