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
            role_type='engaged',
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
            role_type='engaged',
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
            name_en='Test Role',
            name_sv='Test Roll',
            group=self.group,
            role_type='engaged',
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
            name_en='Test Function',
            name_sv='Test Funktion',
            election_email='test@localhost',
            group=self.group,
            role_type='engaged',
        )
        role.teams.add(team)
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

        self.client.get(self.page.url
                        + self.page.reverse_subpage('position', [position.id]))

        self.assertContains(response, team.name,
                            msg_prefix='Position is listed as part of team')
        self.assertContains(response, role.election_email,
                            msg_prefix='Team contact information is provided')

        # TODO: Add tests for my_positions

        # TODO: Add tests for historic positions


class AdminPermissionTests(TestCase):
    """
    Access permission tests for the wagtail admin area of the involvement app.
    These test ensure that admin, fum, board, presidium, group_leader,
    engaged and anonymous
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

    def checkPositions(self, mSet, accepted_types, exclude_actions=[]):
        for action, url in AdminPermissionTests.pages['position'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url)
            else:
                for role_type, position in mSet['approvable_positions'] \
                        .items():
                    if action not in exclude_actions and \
                        (action == 'inspect' or
                            (role_type in accepted_types and
                                action != 'appoint')):
                        self.assertCanAccess(action, url, position,
                                             "%s, %s" % (action, role_type))
                    else:
                        self.assertNoAccess(action, url, position,
                                            "%s, %s" % (action, role_type))

                for role_type, position in mSet['appointable_positions'] \
                        .items():
                    if action not in exclude_actions and \
                        (action == 'inspect' or
                            (role_type in accepted_types and
                                action != 'approve')):
                        self.assertCanAccess(action, url, position,
                                             "%s, %s" % (action, role_type))
                    else:
                        self.assertNoAccess(action, url, position,
                                            "%s, %s" % (action, role_type))

                for role_type, position in mSet['recruiting_positions'] \
                        .items():
                    if action not in exclude_actions and \
                        (action == 'inspect' or
                            (role_type in accepted_types
                                and action not in ['approve', 'appoint'])):
                        self.assertCanAccess(action, url, position,
                                             "%s, %s" % (action, role_type))
                    else:
                        self.assertNoAccess(action, url, position,
                                            "%s, %s" % (action, role_type))

    def checkRoles(self, mSet, accepted_types):
        for action, url in AdminPermissionTests.pages['role'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url)
            else:
                for role_type, role in mSet['roles'].items():
                    if role_type in accepted_types:
                        self.assertCanAccess(action, url, role,
                                             "%s, %s" % (action, role_type))
                    else:
                        self.assertNoAccess(action, url, role,
                                            "%s, %s" % (action, role_type))

    def checkApplications(self, mSet, accepted_types):
        for action, url in AdminPermissionTests.pages['application'].items():
            if action in ['create', 'index']:
                self.assertCanAccess(action, url)
            else:
                for role_type, application in \
                        mSet['submitted_applications'].items():
                    if role_type in accepted_types:
                        self.assertCanAccess(action, url, application)
                    else:
                        self.assertNoAccess(action, url, application,
                                            "%s, %s" % (action, role_type))

    def checkTeams(self, mSet):
        for action, url in AdminPermissionTests.pages['team'].items():
            team = mSet['team']
            self.assertNoAccess(action, url, team, "%s" % (action))

    def all_modals_no_access(self, mSet):
        for action, url in AdminPermissionTests.pages['team'].items():
            if action not in ['index', 'create']:
                team = mSet['team']
                self.assertNoAccess(action, url, team, "%s" % (action))

        for action, url in AdminPermissionTests.pages['application'].items():
            if action not in ['create', 'index']:
                for role_type, application in \
                        mSet['submitted_applications'].items():
                    self.assertNoAccess(action, url, application,
                                        "%s, %s" % (action, role_type))

        for action, url in AdminPermissionTests.pages['role'].items():
            if action not in ['create', 'index']:
                for role_type, role in mSet['roles'].items():
                    self.assertNoAccess(action, url, role,
                                        "%s, %s" % (action, role_type))

        for action, url in AdminPermissionTests.pages['position'].items():
            if action not in ['create', 'index']:
                for role_type, position in mSet['approvable_positions'] \
                                            .items():
                    self.assertNoAccess(action, url, position,
                                        "%s, %s" % (action, role_type))

                for role_type, position in mSet['appointable_positions'] \
                        .items():
                    self.assertNoAccess(action, url, position,
                                        "%s, %s" % (action, role_type))

                for role_type, position in mSet['recruiting_positions'] \
                        .items():
                    self.assertNoAccess(action, url, position,
                                        "%s, %s" % (action, role_type))

    def setUp(self):

        wagtail_access = Permission.objects.get(codename='access_admin')

        role_types = ['admin', 'fum', 'board', 'presidium',
                      'group_leader', 'engaged']

        self.primary_set = {
            'uniq_prefix': 'primary_',
            'members': {},
            'groups': {},
            'roles': {},
            'approvable_positions': {},
            'recruiting_positions': {},
            'appointable_positions': {},
            'submitted_applications': {},
        }

        self.secondary_set = {
            'uniq_prefix': 'secondary_',
            'members': {},
            'groups': {},
            'roles': {},
            'approvable_positions': {},
            'recruiting_positions': {},
            'appointable_positions': {},
            'submitted_applications': {},
        }

        for mSet in [self.primary_set, self.secondary_set]:
            mSet['team'] = Team.objects.create(
                name_en='Team %s en' % mSet['uniq_prefix'],
                name_sv='Team %s sv' % mSet['uniq_prefix'],
            )
            for key in role_types:
                mSet['members'][key] = Member.objects \
                    .create(username="%s%s" % (mSet['uniq_prefix'], key))
                mSet['groups'][key] = Group.objects \
                    .create(name="%s%s" % (mSet['uniq_prefix'], key))
                mSet['groups'][key].permissions.add(wagtail_access)
                mSet['groups'][key].user_set.add(mSet['members'][key])

                mSet['roles'][key] = Role.objects.create(
                    group=mSet['groups'][key],
                    role_type=key,
                    name_en='Role %s en' % "%s%s" % (mSet['uniq_prefix'], key),
                    name_sv='Role %s sv' % "%s%s" % (mSet['uniq_prefix'], key),
                    election_email='%s@localhost' % key,
                )
                mSet['roles'][key].teams.add(mSet['team'])

                currentPosition = Position.objects.create(
                    role=mSet['roles'][key],
                    recruitment_start=date.today() - timedelta(days=5),
                    recruitment_end=date.today() - timedelta(days=1),
                    term_from=date.today() - timedelta(days=5),
                    term_to=date.today() + timedelta(days=365),
                )

                Application.objects.create(
                    position=currentPosition,
                    applicant=mSet['members'][key],
                    status='appointed',
                )

                if key != 'admin':
                    mSet['approvable_positions'][key] = Position.objects \
                        .create(
                            role=mSet['roles'][key],
                            recruitment_start=date.today() - timedelta(days=5),
                            recruitment_end=date.today() - timedelta(days=1),
                            term_from=date.today() + timedelta(days=5),
                            term_to=date.today() + timedelta(days=365),
                        )
                    mSet['recruiting_positions'][key] = Position.objects \
                        .create(
                            role=mSet['roles'][key],
                            recruitment_start=date.today() - timedelta(days=5),
                            recruitment_end=date.today() + timedelta(days=1),
                            term_from=date.today() + timedelta(days=5),
                            term_to=date.today() + timedelta(days=365),
                        )
                    mSet['appointable_positions'][key] = Position.objects \
                        .create(
                            role=mSet['roles'][key],
                            recruitment_start=date.today() - timedelta(days=5),
                            recruitment_end=date.today() - timedelta(days=1),
                            term_from=date.today() + timedelta(days=5),
                            term_to=date.today() + timedelta(days=365),
                        )
                    mSet['submitted_applications'][key] = Application.objects \
                        .create(
                            position=mSet['approvable_positions'][key],
                            applicant=mSet['members'][key],
                            status='submitted',
                        )

    def test_fum(self):
        self.client.force_login(
            self.primary_set['members']['fum'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        self.checkTeams(self.primary_set)

        # Roles
        # Can view and edit roles for role_type 'board'
        self.checkRoles(self.primary_set, ['board'])

        # Position
        # Can view and edit positions for role_type 'board'
        # FUM can never appoint a position
        self.checkPositions(self.primary_set, ['board'], ['appoint'])

        # Applications
        # Can view and edit applications for role_type 'board' and 'presidium'
        self.checkApplications(self.primary_set, ['board', 'presidium'])

        # Make sure that we cant access pages were we are not a team-member
        self.all_modals_no_access(self.secondary_set)

    def test_board(self):
        self.client.force_login(
            self.primary_set['members']['board'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        self.checkTeams(self.primary_set)

        # Roles
        # Can view and edit roles for role_type 'presidium'
        self.checkRoles(self.primary_set, ['presidium'])

        # Position
        # Can view and edit positions for role_type 'presidium'
        self.checkPositions(self.primary_set, ['presidium'])

        # Applications
        # Can view and edit applications for role_type 'presidium'
        self.checkApplications(self.primary_set, ['presidium'])

        # Make sure that we cant access pages were we are not a team-member
        self.all_modals_no_access(self.secondary_set)

    def test_presidium(self):
        self.client.force_login(
            self.primary_set['members']['presidium'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        self.checkTeams(self.primary_set)

        # Roles
        # Can view and edit roles for role_type 'group_leader'
        # and 'engaged'
        self.checkRoles(self.primary_set, ['group_leader', 'engaged'])

        # Position
        # Can view and edit positions for role_type 'group_leader'
        # and 'engaged'
        self.checkPositions(self.primary_set, ['group_leader', 'engaged'])

        # Applications
        # Can view and edit applications for role_type 'group_leader'
        # and 'engaged'
        self.checkApplications(self.primary_set, ['group_leader', 'engaged'])

        # Make sure that we cant access pages were we are not a team-member
        self.all_modals_no_access(self.secondary_set)

    def test_group_leader(self):
        self.client.force_login(
            self.primary_set['members']['group_leader'],
            'django.contrib.auth.backends.ModelBackend'
        )

        # Teams
        # No access to any views
        self.checkTeams(self.primary_set)

        # Roles
        # Can edit roles for role_type 'engaged'
        self.checkRoles(self.primary_set, ['engaged'])

        # Position
        # Can view and edit positions for role_type 'engaged'
        self.checkPositions(self.primary_set, ['engaged'])

        # Applications
        # Can view and edit applications for role_type 'engaged'
        self.checkApplications(self.primary_set, ['engaged'])

        # Make sure that we cant access pages were we are not a team-member
        self.all_modals_no_access(self.secondary_set)

    def test_engaged(self):
        self.client.force_login(
            self.primary_set['members']['engaged'],
            'django.contrib.auth.backends.ModelBackend'
        )

        self.all_modals_no_access(self.primary_set)
        self.all_modals_no_access(self.secondary_set)

    def test_admin(self):
        """
        Tests to ensure admins have access to all parts of the involvement
        admin area
        """
        self.client.force_login(
            self.primary_set['members']['admin'],
            'django.contrib.auth.backends.ModelBackend'
        )
        assert self.primary_set['members']['admin'].is_authenticated

        # Teams
        # Access to all views
        for action, url in AdminPermissionTests.pages['team'].items():
            team = self.primary_set['team']
            self.assertCanAccess(action, url, team, "%s" % (action))

        accepted_roles = ['admin', 'fum', 'board', 'presidium',
                          'group_leader', 'engaged']

        # Roles
        # Access to all views
        self.checkRoles(self.primary_set, accepted_roles)

        # Position
        # Access to all views
        self.checkPositions(self.primary_set, accepted_roles)

        # Applications
        # Access to all views
        self.checkApplications(self.primary_set, accepted_roles)

        # Make sure that we cant access pages were we are not a team-member
        self.all_modals_no_access(self.secondary_set)

    def test_not_logged_in(self):
        """
        Tests to ensure non-users don't have access to the involvement admin
        area
        """
        self.client.logout()

        self.all_modals_no_access(self.primary_set)
        self.all_modals_no_access(self.secondary_set)


class RecruitmentExtensionTestCase(TestCase):
    """
    Tests for the automated deadline extender. The deadline extender should be
    triggered for vacant positions of which the deadline has just passed.
    """
    def setUp(self):

        self.group = Group.objects.create(name='Test Group')
        self.team = Team.objects.create(
            name_en='RecruitmentExtensionTestCase Team EN',
            name_sv='RecruitmentExtensionTestCase Team SV',
        )
        self.role = Role.objects.create(
            name_en='Test',
            name_sv='TestSV',
            role_type='engaged',
            election_email='contact@localhost',
            group=self.group,
        )
        self.role.teams.add(self.team)

        # Create admin group/user
        admin_group = Group.objects.create(
            name='Admin Group',
        )

        self.adminRole = Role.objects.create(
            name_en='Admin Role',
            name_sv='Admin Roll',
            role_type='admin',
            election_email='contact@localhost',
            group=admin_group,
        )
        self.adminRole.teams.add(self.team)

        self.admin = Member.objects.create(
            username='admin',
        )

        adminPos = Position.objects.create(
            role=self.adminRole,
            recruitment_start=date.today() - timedelta(days=5),
            recruitment_end=date.today() - timedelta(days=1),
            term_from=date.today() - timedelta(days=5),
            term_to=date.today() + timedelta(days=365),
        )

        self.adminApplication = Application.objects.create(
            position=adminPos,
            applicant=self.admin,
            status='appointed',
        )

        wagtail_access = Permission.objects.get(codename='access_admin')
        admin_group.permissions.add(wagtail_access)
        admin_group.user_set.add(self.admin)
        admin_group.save()
        self.client.force_login(
            self.admin, 'django.contrib.auth.backends.ModelBackend'
        )

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


class RecruitmentExtensionEmailTestCase(TestCase):
    """
    Tests for the automated deadline extender emails. The deadline extender
    should be triggered for vacant positions of which the deadline has just
    passed.
    """

    def setUp(self):
        self.group = Group.objects.create(name='Test Group')
        self.team = Team.objects.create(
            name_en='RecruitmentExtensionTestCase Team EN',
            name_sv='RecruitmentExtensionTestCase Team SV',
        )
        self.role = Role.objects.create(
            name_en='Test',
            name_sv='TestSV',
            role_type='engaged',
            election_email='contact@localhost',
            group=self.group,
        )
        self.role.teams.add(self.team)

        self.member = Member.objects.create(
            username='member',
        )

    def test_send_email(self):
        """
        Test that an e-mail is being send when the deadline for an position
        passes without any applications.
        """
        mail.outbox.clear()
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
        mail.outbox.clear()
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
            applicant=self.member,
            status='submitted',
        )

        send_extension_emails()

        self.assertEqual(len(mail.outbox), 0)
