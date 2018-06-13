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
    Application
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
        self.group = Group.objects.create(name='RecruitmentPageTests Group')
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
            group=self.group,
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
            group=self.group,
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
            group=self.group,
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
        )
        role = Role.objects.create(
            team=team,
            name_en='Test Function',
            name_sv='Test Funktion',
            election_email='test@localhost',
            group=self.group,
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

        # TODO: Add tests for historic positions


class AdminPermissionTests(TestCase):
    """
    Access permission tests for the wagtail admin area of the involvement app.
    These test ensure that admin, fum, board, bureau, group_leader, engaged and anonymous
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

    def assertCanAccess(self, action, url, obj=None, err_msg=''):
        if action in ['create', 'index'] or obj is None:
            self.assertCanAccess_(reverse(url), err_msg)
        else:
            self.assertCanAccess_(reverse(url, args=[obj.pk]), err_msg)

    def assertNoAccess(self, action, url, obj=None, err_msg=''):
        if action in ['create', 'index'] or obj is None:
            self.assertNoAccess_(reverse(url), err_msg)
        else:
            self.assertNoAccess_(reverse(url, args=[obj.pk]), err_msg)

    def assertCanAccess_(self, url, err_msg=''):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         "Unable to access '%s'. %s" % (url, err_msg))
        return response

    def assertNoAccess_(self, url, err_msg=''):
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302],
                      "'%s' should not be accessible. %s" % (url, err_msg))
        return response

    # Check each type of position for access.
    #
    # create, index and inspect should always be accessible.
    # accepted_codenames defines when a position should be accessible
    # for modification
    def checkPositions(self, accepted_codenames, exclude_actions=[]):
        for action, url in AdminPermissionTests.pages['position'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url)
            else:
                for codename, position in self.approvable_positions.items():
                    if action not in exclude_actions and \
                        (action == 'inspect' or
                            (codename in accepted_codenames and
                                action != 'appoint')):
                        self.assertCanAccess(action, url, position,
                                             "%s, %s" % (action, codename))
                    else:
                        self.assertNoAccess(action, url, position,
                                            "%s, %s" % (action, codename))

                for codename, position in self.appointable_positions.items():
                    if action not in exclude_actions and \
                        (action == 'inspect' or
                            (codename in accepted_codenames and
                                action != 'approve')):
                        self.assertCanAccess(action, url, position,
                                             "%s, %s" % (action, codename))
                    else:
                        self.assertNoAccess(action, url, position,
                                            "%s, %s" % (action, codename))

                for codename, position in self.recruiting_positions.items():
                    if action not in exclude_actions and \
                        (action == 'inspect' or
                            (codename in accepted_codenames
                                and action not in ['approve', 'appoint'])):
                        self.assertCanAccess(action, url, position,
                                             "%s, %s" % (action, codename))
                    else:
                        self.assertNoAccess(action, url, position,
                                            "%s, %s" % (action, codename))

    def checkRoles(self, accepted_codenames):
        for action, url in AdminPermissionTests.pages['role'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url)
            else:
                for codename, role in self.roles.items():
                    if codename in accepted_codenames:
                        self.assertCanAccess(action, url, role,
                                             "%s, %s" % (action, codename))
                    else:
                        self.assertNoAccess(action, url, role,
                                            "%s, %s" % (action, codename))

    def checkApplications(self, accepted_codenames):
        for action, url in AdminPermissionTests.pages['application'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url)
            else:
                for codename, application in \
                        self.submitted_applications.items():
                    if codename in accepted_codenames:
                        self.assertCanAccess(action, url, application)
                    else:
                        self.assertNoAccess(action, url, application,
                                            "%s, %s" % (action, codename))

    def checkTeams(self, accepted_codenames):
        for action, url in AdminPermissionTests.pages['team'].items():
            for codename, team in self.teams.items():
                if codename in accepted_codenames:
                    self.assertCanAccess(action, url, team)
                else:
                    self.assertNoAccess(action, url, team,
                                        "%s, %s" % (action, codename))

    def setUp(self):

        wagtail_access = Permission.objects.get(codename='access_admin')

        permission_codenames = ['admin', 'fum', 'board', 'bureau',
                                'group_leader', 'engaged']

        self.members = {}
        self.groups = {}
        self.teams = {}
        self.roles = {}
        self.approvable_positions = {}
        self.recruiting_positions = {}
        self.appointable_positions = {}
        self.submitted_applications = {}

        for key in permission_codenames:
            self.members[key] = Member.objects.create(username=key)
            permission = Permission.objects.get(codename=key)
            self.groups[key] = Group.objects.create(name=key)
            self.groups[key].permissions.add(wagtail_access)
            self.groups[key].permissions.add(permission)
            self.groups[key].user_set.add(self.members[key])

            if key != 'admin':
                self.teams[key] = Team.objects.create(
                    name_en='Team %s en' % key,
                    name_sv='Team %s sv' % key,
                )
                self.roles[key] = Role.objects.create(
                    team=self.teams[key],
                    group=self.groups[key],
                    name_en='Role %s en' % key,
                    name_sv='Role %s sv' % key,
                    election_email='%s@localhost' % key,
                )
                self.approvable_positions[key] = Position.objects.create(
                    role=self.roles[key],
                    recruitment_start=date.today() - timedelta(days=5),
                    recruitment_end=date.today() - timedelta(days=1),
                    term_from=date.today() + timedelta(days=5),
                    term_to=date.today() + timedelta(days=365),
                )
                self.recruiting_positions[key] = Position.objects.create(
                    role=self.roles[key],
                    recruitment_start=date.today() - timedelta(days=5),
                    recruitment_end=date.today() + timedelta(days=1),
                    term_from=date.today() + timedelta(days=5),
                    term_to=date.today() + timedelta(days=365),
                )
                self.appointable_positions[key] = Position.objects.create(
                    role=self.roles[key],
                    recruitment_start=date.today() - timedelta(days=5),
                    recruitment_end=date.today() - timedelta(days=1),
                    term_from=date.today() + timedelta(days=5),
                    term_to=date.today() + timedelta(days=365),
                )
                self.submitted_applications[key] = Application.objects.create(
                    position=self.approvable_positions[key],
                    applicant=self.members[key],
                    status='submitted',
                )

    def test_fum(self):
        self.client.force_login(
            self.members['fum'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        self.checkTeams([])

        # Roles
        # Can view and edit roles for codename 'board'
        self.checkRoles(['board'])

        # Position
        # Can view and edit positions for codename 'board'
        # FUM can never appoint a position
        self.checkPositions(['board'], ['appoint'])

        # Applications
        # Can view and edit applications for codename 'board' and 'bureau'
        self.checkApplications(['board', 'bureau'])

    def test_board(self):
        self.client.force_login(
            self.members['board'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        self.checkTeams([])

        # Roles
        # Can view and edit roles for codename 'bureau'
        self.checkRoles(['bureau'])

        # Position
        # Can view and edit positions for codename 'bureau'
        self.checkPositions(['bureau'])

        # Applications
        # Can view and edit applications for codename 'bureau'
        self.checkApplications(['bureau'])

    def test_bureau(self):
        self.client.force_login(
            self.members['bureau'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        self.checkTeams([])

        # Roles
        # Can view and edit roles for codename 'group_leader'
        # and 'engaged'
        self.checkRoles(['group_leader', 'engaged'])

        # Position
        # Can view and edit positions for codename 'group_leader'
        # and 'engaged'
        self.checkPositions(['group_leader', 'engaged'])

        # Applications
        # Can view and edit applications for codename 'group_leader'
        # and 'engaged'
        self.checkApplications(['group_leader', 'engaged'])

    def test_group_leader(self):
        self.client.force_login(
            self.members['group_leader'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        self.checkTeams([])

        # Roles
        # Can edit roles for codename 'engaged'
        self.checkRoles(['engaged'])

        # Position
        # Can view and edit positions for codename 'engaged'
        self.checkPositions(['engaged'])

        # Applications
        # Can view and edit applications for codename 'engaged'
        self.checkApplications(['engaged'])

    def test_engaged(self):
        self.client.force_login(
            self.members['engaged'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        for action, url in AdminPermissionTests.pages['team'].items():
            if action in ['create', 'index']:
                self.assertNoAccess(action, url)
            else:
                for codename, team in self.teams.items():
                    self.assertNoAccess(action, url, team)

        # Roles
        # No access to any views
        for action, url in AdminPermissionTests.pages['role'].items():
            if action in ['create', 'index']:
                self.assertNoAccess(action, url)
            else:
                for codename, role in self.roles.items():
                    self.assertNoAccess(action, url, role)

        # Position
        # No access to any views
        for action, url in AdminPermissionTests.pages['position'].items():
            if action in ['create', 'index']:
                self.assertNoAccess(action, url)
            else:
                for codename, position in self.approvable_positions.items():
                    self.assertNoAccess(action, url, position)

        # Applications
        # No access to any views
        for action, url in AdminPermissionTests.pages['application'].items():
            if action in ['create', 'index']:
                self.assertNoAccess(action, url)
            else:
                for codename, application in \
                        self.submitted_applications.items():
                    self.assertNoAccess(action, url, application)

    def test_admin(self):
        """
        Tests to ensure admins have access to all parts of the involvement
        admin area
        """
        self.client.force_login(
            self.members['admin'],
            'django.contrib.auth.backends.ModelBackend'
        )
        assert self.members['admin'].is_authenticated

        # Teams
        # Access to all views
        for action, url in AdminPermissionTests.pages['team'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url, None)
            else:
                for codename, team in self.teams.items():
                    self.assertCanAccess(action, url, team)

        # Roles
        # Access to all views
        for action, url in AdminPermissionTests.pages['role'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url, None)
            else:
                for codename, role in self.roles.items():
                    self.assertCanAccess(action, url, role)

        # Position
        # Access to all views
        for action, url in AdminPermissionTests.pages['position'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url, None)
            else:
                for codename, position in self.approvable_positions.items():
                    self.assertCanAccess(action, url, position)

        # Applications
        # Access to all views
        for action, url in AdminPermissionTests.pages['application'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url, None)
            else:
                for codename, application in \
                        self.submitted_applications.items():
                    self.assertCanAccess(action, url, application)

    def test_not_logged_in(self):
        """
        Tests to ensure non-users don't have access to the involvement admin
        area
        """
        self.client.logout()

        # Tests that don't require an instance.
        for i, section in AdminPermissionTests.pages.items():
            for action, url in section.items():
                if action in ['create', 'index']:
                    self.assertNoAccess(action, url)

        # Teams
        # No access to any views
        for action, url in AdminPermissionTests.pages['team'].items():
            if action in ['create', 'index']:
                self.assertNoAccess(action, url)
            else:
                for codename, team in self.teams.items():
                    self.assertNoAccess(action, url, team)

        # Roles
        # No access to any views
        for action, url in AdminPermissionTests.pages['role'].items():
            if action in ['create', 'index']:
                self.assertNoAccess(action, url)
            else:
                for codename, role in self.roles.items():
                    self.assertNoAccess(action, url, role)

        # Position
        # No access to any views
        for action, url in AdminPermissionTests.pages['position'].items():
            if action in ['create', 'index']:
                self.assertNoAccess(action, url)
            else:
                for codename, position in self.approvable_positions.items():
                    self.assertNoAccess(action, url, position)

        # Applications
        # No access to any views
        for action, url in AdminPermissionTests.pages['application'].items():
            if action in ['create', 'index']:
                self.assertNoAccess(action, url)
            else:
                for codename, application in \
                        self.submitted_applications.items():
                    self.assertNoAccess(action, url, application)


class RecruitmentExtensionTestCase(TestCase):
    """
    Tests for the automated deadline extender. The deadline extender should be
    triggered for vacant positions of which the deadline has just passed.
    """

    def setUp(self):
        self.group = Group.objects.create(name='Test Group')
        self.role = Role.objects.create(
            name_en='Test',
            name_sv='TestSV',
            election_email='contact@localhost',
            group=self.group,
        )

        # Create admin group/user
        wagtail_acces = Permission.objects.get(codename='access_admin')
        recruitment_admin = Permission.objects.get(
            codename='admin'
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
