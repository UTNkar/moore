from django.test import TestCase
from datetime import datetime

from members.models import Member, StudyProgram


class MemberTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(username='test')
        self.assertEqual(1, Member.objects.count())

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
