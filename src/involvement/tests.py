from datetime import date, timedelta

from django.contrib.auth.models import Group, Permission
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from home.models import HomePage
from involvement.cron import send_extension_emails
from involvement.models import RecruitmentPage, Position, Role, Team, \
    Application, CurrentMandate
from members.models import Member


class RecruitmentPageTests(WagtailPageTests):
    def setUp(self):
        self.login()

        parent = Page.objects.get(url_path='/home/')
        self.page = RecruitmentPage(
            title='Apply now!',
            title_sv='Ansök nu!',
            slug='apply'
        )
        parent.add_child(instance=self.page)

    def test_can_create_page(self):
        parent = Page.get_root_nodes()[0]

        # Assert that a RecruitmentPage can be made here, with this POST data
        self.assertCanCreate(parent, RecruitmentPage, {
            'title': 'Apply now!',
            'title_sv': 'Ansök nu!',
            'slug': 'apply2',
        }, 'Recruitment pages can be created at the root')

    def test_can_create_under_home_page(self):
        """
        It is possible to create a recruitment page with a home page as its
        parent.
        """
        self.assertCanCreateAt(HomePage, RecruitmentPage)

    def test_open_positions_empty(self):
        """
        If there are no open positions, an appropriate message should be
        displayed.
        """
        response = self.client.get(
            self.page.url + self.page.reverse_subpage('open_positions')
        )

        self.assertEqual(response.status_code, 200,
                         msg='You can open the positions page')
        self.assertContains(response, 'There are currently no open positions. '
                                      'Check back later!')
        self.assertQuerysetEqual(response.context['positions'], [],
                                 msg='Response context does not contain'
                                     ' positions')

    def test_open_positions_one_position(self):
        """
        When there are open positions, these positions should be visible and
        a link should be available to their specific page.
        """
        role = Role.objects.create(
            name_en='Test Role',
            name_sv='Test Roll',
        )
        position = Position.objects.create(
            role=role,
            recruitment_start=date.today() - timedelta(days=1),
            recruitment_end=date.today(),
            term_from=date.today() + timedelta(days=1),
            term_to=date.today() + timedelta(days=365),
        )
        response = self.client.get(
            self.page.url + self.page.reverse_subpage('open_positions')
        )

        self.assertEqual(response.status_code, 200,
                         'You can open the positions page')
        self.assertContains(response, position.__str__(),
                            msg_prefix='Response contains position name')
        self.assertContains(
            response,
            self.page.url + self.page.reverse_subpage(
                'position',
                [position.id]
            ),
            msg_prefix='Response contains position URL'
        )
        self.assertQuerysetEqual(response.context['positions'],
                                 ['<Position: ' + position.__str__() + '>'],
                                 msg='Response context contains the position')

    def test_position_view_general(self):
        role = Role.objects.create(
            name_en='Test Role',
            name_sv='Test Roll',
        )
        position = Position.objects.create(
            role=role,
            recruitment_start=date.today() - timedelta(days=1),
            recruitment_end=date.today(),
            term_from=date.today() + timedelta(days=1),
            term_to=date.today() + timedelta(days=365),
        )
        response = self.client.get(self.page.url + self.page.reverse_subpage(
            'position',
            [position.id]
        ))

        self.assertEqual(response.status_code, 200,
                         msg='You can open the position page')
        self.assertContains(response, position.__str__(),
                            msg_prefix='Response contains position name')
        self.assertEqual(response.context['position'],
                         position,
                         msg='Response context contains the position')

    def test_position_view_unaffiliated(self):
        role = Role.objects.create(
            team=None,
            name_en='Test Role',
            name_sv='Test Roll',
        )
        position = Position.objects.create(
            role=role,
            recruitment_start=date.today() - timedelta(days=1),
            recruitment_end=date.today(),
            term_from=date.today() + timedelta(days=1),
            term_to=date.today() + timedelta(days=365),
        )
        response = self.client.get(self.page.url + self.page.reverse_subpage(
            'position',
            [position.id]
        ))

        self.assertContains(response, 'Unaffiliated',
                            msg_prefix='Position is listed as unaffiliated')

    def test_position_view_team(self):
        team = Team.objects.create(
            name_en='Test Team',
            name_sv='Testteam',
            group=Group.objects.first()
        )
        role = Role.objects.create(
            team=team,
            name_en='Test Function',
            name_sv='Test Funktion',
            election_email='test@localhost',
        )
        position = Position.objects.create(
            role=role,
            recruitment_start=date.today() - timedelta(days=1),
            recruitment_end=date.today(),
            term_from=date.today() + timedelta(days=1),
            term_to=date.today() + timedelta(days=365),
        )
        response = self.client.get(self.page.url + self.page.reverse_subpage(
            'position',
            [position.id]
        ))

        self.assertContains(response, team.name,
                            msg_prefix='Position is listed as part of team')
        self.assertContains(response, role.election_email,
                            msg_prefix='Team contact information is provided')

        # TODO: Add tests for my_positions


class AdminPermissionTests(TestCase):
    """
    Access permission tests for the wagtail admin area of the involvement app.
    These test ensure that admins, officials, election members and anonymous
    users have the appropriate amount of access.
    """
    pages = {
        'team': {
            'index': 'involvement_team_modeladmin_index',
            'create': 'involvement_team_modeladmin_create',
            'inspect': 'involvement_team_modeladmin_inspect',
            'edit': 'involvement_team_modeladmin_edit',
            'delete': 'involvement_team_modeladmin_delete',
        },
        'role': {
            'index': 'involvement_role_modeladmin_index',
            'create': 'involvement_role_modeladmin_create',
            'edit': 'involvement_role_modeladmin_edit',
            'delete': 'involvement_role_modeladmin_delete',
        },
        'position': {
            'index': 'involvement_position_modeladmin_index',
            'create': 'involvement_position_modeladmin_create',
            'inspect': 'involvement_position_modeladmin_inspect',
            'edit': 'involvement_position_modeladmin_edit',
            'delete': 'involvement_position_modeladmin_delete',
            'appoint': 'involvement_position_modeladmin_appoint',
            'approve': 'involvement_position_modeladmin_approve',
        },
        'application': {
            'index': 'involvement_application_modeladmin_index',
            'create': 'involvement_application_modeladmin_create',
            'edit': 'involvement_application_modeladmin_edit',
            'delete': 'involvement_application_modeladmin_delete',
        }
    }

    def assertCanAccess(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         "Unable to access '%s'" % url)
        return response

    def assertNoAccess(self, url):
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302],
                      "'%s' should not be accessible" % url)
        return response

    def setUp(self):
        """
        Create users, teams, and groups for use in other tests
        """
        wagtail_access = Permission.objects.get(
            name='Can access Wagtail admin'
        )
        recruitment_admin = Permission.objects.get(
            name='Can administrate the recruitment process'
        )

        # Create standard team + official
        self.group = Group.objects.create(
            name='Test Team',
        )
        self.group.permissions.add(wagtail_access)
        self.team = Team.objects.create(
            name_en='Test Team',
            name_sv='Testteam',
            group=self.group
        )
        self.official = Member.objects.create(
            username='official',
        )
        self.role = Role.objects.create(
            team=self.team,
            name_en='Test Function',
            name_sv='Test Funktion',
            election_email='test@localhost',
            official=True,
        )
        self.position = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=2),
            recruitment_end=date.today() - timedelta(days=2),
            term_from=date.today() - timedelta(days=1),
            term_to=date.today() + timedelta(days=365),
        )
        self.official_application = Application.objects.create(
            position=self.position,
            applicant=self.official,
            status='appointed',
        )
        self.current_mandate = CurrentMandate.objects.create(
            position=self.position,
            applicant=self.official
        )
        self.group.user_set.add(self.official)
        self.group.save()

        # Create admin group/user
        self.admin_group = Group.objects.create(
            name='Admin Group',
        )
        self.admin_group.permissions.add(wagtail_access, recruitment_admin)
        self.admin = Member.objects.create(
            username='admin',
        )
        self.admin_group.user_set.add(self.admin)
        self.admin_group.save()

        # Create other team + user to be user as election committee
        self.approval_group = Group.objects.create(
            name='Approval Team',
        )
        self.approval_group.permissions.add(wagtail_access)
        self.approval_team = Team.objects.create(
            name_en='Approval Team',
            name_sv='Approval Team',
            group=self.approval_group
        )
        self.approver = Member.objects.create(
            username='approver',
        )
        self.approval_group.user_set.add(self.approver)
        self.approval_group.save()

        # Create basic member
        self.member = Member.objects.create(
            username='member',
        )

        # Create secondary position
        self.group2 = Group.objects.create(
            name='Secondary Team',
        )
        self.team2 = Team.objects.create(
            name_en='Secondary Team',
            name_sv='SecondaryTeam',
            group=self.group2
        )
        self.role2 = Role.objects.create(
            team=self.team2,
            name_en='Secondary group',
            name_sv='Secondarygroup',
            election_email='test@localhost',
            official=True,
        )
        self.position2 = Position.objects.create(
            role=self.role2,
            recruitment_start=date.today() - timedelta(days=2),
            recruitment_end=date.today() - timedelta(days=2),
            term_from=date.today() - timedelta(days=1),
            term_to=date.today() + timedelta(days=365),
        )

        self.member_application = Application.objects.create(
            position=self.position2,
            applicant=self.member,
            status='appointed',
        )

    def test_not_logged_in(self):
        """
        Tests to ensure non-users don't have access to the involvement admin
        area
        """
        # Tests that don't require an instance.
        for i, section in AdminPermissionTests.pages.items():
            for action, url in section.items():
                if action in ['create', 'index']:
                    self.assertNoAccess(reverse(url))

        # Tests for team specific pages
        for action, url in AdminPermissionTests.pages['team'].items():
            if action not in ['create', 'index']:
                self.assertNoAccess(reverse(url, args=[self.team.pk]))

        # Tests for role specific pages
        for action, url in AdminPermissionTests.pages['role'].items():
            if action not in ['create', 'index']:
                self.assertNoAccess(reverse(url, args=[self.role.pk]))

        # Tests for position specific pages
        for action, url in AdminPermissionTests.pages['position'].items():
            if action not in ['create', 'index']:
                self.assertNoAccess(reverse(url, args=[self.position.pk]))

        # Tests for application specific pages
        for action, url in AdminPermissionTests.pages['application'].items():
            if action not in ['create', 'index']:
                self.assertNoAccess(reverse(url,
                                    args=[self.official_application.pk]))

    def test_admin(self):
        """
        Tests to ensure admins have access to all parts of the involvement
        admin area
        """
        self.client.force_login(
            self.admin, 'django.contrib.auth.backends.ModelBackend'
        )
        assert self.admin.is_authenticated
        for i, section in AdminPermissionTests.pages.items():
            for action, url in section.items():
                if action in ['create', 'index']:
                    self.assertCanAccess(reverse(url))

        for action, url in AdminPermissionTests.pages['team'].items():
            if action not in ['create', 'index']:
                self.assertCanAccess(reverse(url, args=[self.team.pk]))

        for action, url in AdminPermissionTests.pages['role'].items():
            if action not in ['create', 'index']:
                self.assertCanAccess(reverse(url, args=[self.role.pk]))

        for action, url in AdminPermissionTests.pages['position'].items():
            if action not in ['create', 'index']:
                self.assertCanAccess(reverse(url, args=[self.position.pk]))

        for action, url in AdminPermissionTests.pages['application'].items():
            if action not in ['create', 'index']:
                self.assertCanAccess(reverse(url,
                                     args=[self.official_application.pk]))

    def test_official(self):
        """
        Tests to ensure officials have access to admin parts that involve only
        their team.
        """
        self.client.force_login(
            self.official, 'django.contrib.auth.backends.ModelBackend'
        )
        # Tests for team pages
        for action, url in AdminPermissionTests.pages['team'].items():
            if action == 'index':
                response = self.assertCanAccess(reverse(url))
                self.assertContains(response, self.team.name)
                self.assertNotContains(response, self.approval_team.name)
            elif action in ['inspect', 'edit']:
                self.assertCanAccess(reverse(url, args=[self.team.pk]))
                self.assertNoAccess(reverse(url, args=[self.approval_team.pk]))
            elif action == 'delete':
                self.assertNoAccess(reverse(url, args=[self.team.pk]))
                self.assertNoAccess(reverse(url, args=[self.approval_team.pk]))
            elif action == 'create':
                self.assertNoAccess(reverse(url))

        # Tests for role pages
        other_role = Role.objects.create(
            team=self.approval_team,
            name_en='Other',
            name_sv='Other SV',
        )
        for action, url in AdminPermissionTests.pages['role'].items():
            if action == 'index':
                response = self.assertCanAccess(reverse(url))
                self.assertContains(response, self.role.name)
                self.assertNotContains(response, other_role.name)
            elif action == 'edit':
                self.assertCanAccess(reverse(url, args=[self.role.pk]))
                self.assertNoAccess(reverse(url, args=[other_role.pk]))
            elif action == 'delete':
                self.assertNoAccess(reverse(url, args=[self.role.pk]))
                self.assertNoAccess(reverse(url, args=[other_role.pk]))
            elif action == 'create':
                self.assertCanAccess(reverse(url))

        # Tests for position pages
        other_position = Position.objects.create(
            role=other_role,
            recruitment_start=date.today(),
            recruitment_end=date.today(),
            term_from=date.today(),
            term_to=date.today(),
        )
        drafted_position = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() + timedelta(days=2),
            recruitment_end=date.today() + timedelta(days=5),
            term_from=date.today() + timedelta(days=10),
            term_to=date.today() + timedelta(days=365),
        )
        recruiting_position = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=2),
            recruitment_end=date.today() + timedelta(days=3),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        approved_position = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=5),
            recruitment_end=date.today() - timedelta(days=1),
            term_from=date.today() + timedelta(days=1),
            term_to=date.today() + timedelta(days=365),
        )
        for action, url in AdminPermissionTests.pages['position'].items():
            if action == 'index':
                response = self.assertCanAccess(reverse(url))
                self.assertContains(response, self.position.role.name,
                                    count=4)
                self.assertNotContains(response, other_position.role.name)
            elif action == 'inspect':
                self.assertCanAccess(reverse(url, args=[self.position.pk]))
                self.assertCanAccess(reverse(url, args=[drafted_position.pk]))
                self.assertCanAccess(
                    reverse(url, args=[recruiting_position.pk])
                )
                self.assertCanAccess(reverse(url, args=[approved_position.pk]))
                self.assertNoAccess(reverse(url, args=[other_position.pk]))
            elif action == 'edit':
                self.assertCanAccess(reverse(url, args=[self.position.pk]))
                self.assertCanAccess(reverse(url, args=[drafted_position.pk]))
                self.assertCanAccess(
                    reverse(url, args=[recruiting_position.pk])
                )
                self.assertCanAccess(reverse(url, args=[approved_position.pk]))
                self.assertNoAccess(reverse(url, args=[other_position.pk]))
            elif action == 'delete':
                self.assertNoAccess(reverse(url, args=[self.position.pk]))
                self.assertCanAccess(reverse(url, args=[drafted_position.pk]))
                self.assertNoAccess(
                    reverse(url, args=[recruiting_position.pk])
                )
                self.assertNoAccess(reverse(url, args=[approved_position.pk]))
                self.assertNoAccess(reverse(url, args=[other_position.pk]))
            elif action == 'create':
                self.assertCanAccess(reverse(url))
            elif action == 'approve':
                self.assertNoAccess(reverse(url, args=[self.position.pk]))
                self.assertNoAccess(reverse(url, args=[drafted_position.pk]))
                self.assertNoAccess(
                    reverse(url, args=[recruiting_position.pk])
                )
                self.assertNoAccess(reverse(url, args=[approved_position.pk]))
                self.assertNoAccess(reverse(url, args=[other_position.pk]))
            elif action == 'appoint':
                self.assertNoAccess(reverse(url, args=[self.position.pk]))
                self.assertNoAccess(reverse(url, args=[drafted_position.pk]))
                self.assertNoAccess(
                    reverse(url, args=[recruiting_position.pk])
                )
                self.assertCanAccess(
                    reverse(url, args=[approved_position.pk])
                )
                self.assertNoAccess(reverse(url, args=[other_position.pk]))

        # Tests for application pages
        for action, url in AdminPermissionTests.pages['application'].items():
            if action in ['index', 'create']:
                self.assertCanAccess(reverse(url))
            elif action in ['edit', 'delete']:
                # Only accessible by official or admin
                self.assertCanAccess(reverse(url,
                                     args=[self.official_application.pk]))
                self.assertNoAccess(reverse(url,
                                    args=[self.member_application.pk]))

    def test_approver(self):
        """
        Tests that ensure that approvers have access just to the position
        pages/instances under their  approval
        """
        self.client.force_login(
            self.approver, 'django.contrib.auth.backends.ModelBackend'
        )

        # Tests that don't require an instance.
        for i, section in AdminPermissionTests.pages.items():
            for action, url in section.items():
                if action in ['create', 'index'] \
                        and not (i == 'position' and action == 'index'):
                    self.assertNoAccess(reverse(url))

        # Tests for team specific pages
        for action, url in AdminPermissionTests.pages['team'].items():
            if action not in ['create', 'index']:
                self.assertNoAccess(reverse(url, args=[self.team.pk]))

        # Tests for role specific pages
        for action, url in AdminPermissionTests.pages['role'].items():
            if action not in ['create', 'index']:
                self.assertNoAccess(reverse(url, args=[self.role.pk]))

        # Tests for application specific pages
        for action, url in AdminPermissionTests.pages['application'].items():
            if action not in ['create', 'index']:
                self.assertNoAccess(reverse(url,
                                    args=[self.official_application.pk]))

        # Tests for position specific pages
        recruiting_position = Position.objects.create(
            role=self.role,
            approval_committee=self.approval_team,
            recruitment_start=date.today() - timedelta(days=2),
            recruitment_end=date.today() + timedelta(days=3),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        ready_position = Position.objects.create(
            role=self.role,
            approval_committee=self.approval_team,
            recruitment_start=date.today() - timedelta(days=5),
            recruitment_end=date.today() - timedelta(days=1),
            term_from=date.today() + timedelta(days=1),
            term_to=date.today() + timedelta(days=365),
        )
        Application.objects.create(
            position=ready_position,
            applicant=self.official,
            status='submitted',
        )
        for action, url in AdminPermissionTests.pages['position'].items():
            if action == 'index':
                response = self.assertCanAccess(reverse(url))
                self.assertContains(response, self.role.name, count=2)
            elif action in 'approve':
                self.assertNoAccess(reverse(url, args=[self.position.pk]))
                self.assertNoAccess(
                    reverse(url, args=[recruiting_position.pk])
                )
                self.assertCanAccess(reverse(url, args=[ready_position.pk]))
            elif action in 'inspect':
                self.assertNoAccess(reverse(url, args=[self.position.pk]))
                self.assertCanAccess(
                    reverse(url, args=[recruiting_position.pk])
                )
                self.assertCanAccess(reverse(url, args=[ready_position.pk]))
            elif action in ['edit', 'appoint', 'delete']:
                self.assertNoAccess(reverse(url, args=[self.position.pk]))
                self.assertNoAccess(
                    reverse(url, args=[recruiting_position.pk])
                )
                self.assertNoAccess(reverse(url, args=[ready_position.pk]))


class RecruitmentExtensionTestCase(TestCase):
    """
    Tests for the automated deadline extender. The deadline extender should be
    triggered for vacant positions of which the deadline has just passed.
    """

    def setUp(self):
        self.role = Role.objects.create(
            name_en='Test',
            name_sv='TestSV',
            election_email='contact@localhost',
        )

        # Create admin group/user
        wagtail_acces = Permission.objects.get(name='Can access Wagtail admin')
        recruitment_admin = Permission.objects.get(
            name='Can administrate the recruitment process'
        )
        admin_group = Group.objects.create(
            name='Admin Group',
        )
        admin_group.permissions.add(wagtail_acces, recruitment_admin)
        self.admin = Member.objects.create(
            username='admin',
        )
        mail.outbox.clear()
        admin_group.user_set.add(self.admin)
        admin_group.save()
        self.client.force_login(
            self.admin, 'django.contrib.auth.backends.ModelBackend'
        )

    def test_send_email(self):
        """
        Test that an e-mail is being send when the deadline for an position
        passes without any applications.
        """
        pos = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=10),
            recruitment_end=date.today() - timedelta(days=1),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        send_extension_emails()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.role.election_email])
        self.assertIn(
            reverse('involvement_position_extend', args=[pos.pk]),
            mail.outbox[0].body
        )

    def test_no_email(self):
        """
        Test that no e-mails are being send when the deadline has not passed or
        when there are applications
        """
        Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=10),
            recruitment_end=date.today(),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        applied = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=10),
            recruitment_end=date.today() - timedelta(days=1),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        Application.objects.create(
            position=applied,
            applicant=self.admin,
            status='submitted',
        )

        send_extension_emails()

        self.assertEqual(len(mail.outbox), 0)

    def test_extension(self):
        """Test automatic extension urls"""
        pos = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=10),
            recruitment_end=date.today() - timedelta(days=1),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        response = self.client.get(
            reverse('involvement_position_extend', args=[pos.pk]))
        self.assertRedirects(response,
                             reverse('involvement_position_modeladmin_index'))

        pos.refresh_from_db()
        self.assertGreater(pos.recruitment_end, date.today())

    def test_no_access(self):
        """Test denial of automatic extension when user has no access."""
        self.client.logout()

        pos = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=10),
            recruitment_end=date.today() - timedelta(days=1),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        response = self.client.get(
            reverse('involvement_position_extend', args=[pos.pk]))
        self.assertEqual(response.status_code, 302)

    def test_not_ended(self):
        """
        Test denial of automatic extension when recruitment has not ended
        """
        recruiting = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=10),
            recruitment_end=date.today(),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        response = self.client.get(
            reverse('involvement_position_extend', args=[recruiting.pk]))
        self.assertRedirects(response,
                             reverse('involvement_position_modeladmin_index'))

        recruiting.refresh_from_db()
        self.assertEqual(recruiting.recruitment_end, date.today())

    def test_with_applications(self):
        """
        Test denial of automatic extension when members have applied
        """
        applied = Position.objects.create(
            role=self.role,
            recruitment_start=date.today() - timedelta(days=10),
            recruitment_end=date.today() - timedelta(days=1),
            term_from=date.today() + timedelta(days=4),
            term_to=date.today() + timedelta(days=365),
        )
        Application.objects.create(
            position=applied,
            applicant=self.admin,
            status='submitted',
        )
        response = self.client.get(
            reverse('involvement_position_extend', args=[applied.pk]))
        self.assertRedirects(response,
                             reverse('involvement_position_modeladmin_index'))

        applied.refresh_from_db()
        self.assertEqual(
            applied.recruitment_end, date.today() - timedelta(days=1)
        )
