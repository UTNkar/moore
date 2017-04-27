from datetime import date, timedelta

from django.contrib.auth.models import Group
from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from home.models import HomePage
from involvement.models import RecruitmentPage, Position, Role, Team


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
