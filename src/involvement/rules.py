import rules
from involvement.models import Role
from involvement.rule_utils import is_super, is_admin, is_fum, \
    is_board, has_role_perm


# Contact card predicates
@rules.predicate
def member_of_team_contactcard(user, card):
    return card is not None and member_of_team_role(user, card.position.role)


@rules.predicate
def can_modify_contactcard(user, card):
    return card is not None and can_set_applicant(user, card.position)


# Application predicates
@rules.predicate
def member_of_team_appl(user, application):
    return member_of_team_role(user, application.position.role)


@rules.predicate
def can_modify_application(user, application):
    return can_set_applicant(user, application.position)


# Position predicates
@rules.predicate
def member_of_team_position(user, position):
    return member_of_team_role(user, position.role)


@rules.predicate
def is_action_approve(user, position):
    return position.current_action() == 'approve'


@rules.predicate
def is_action_appoint(user, position):
    return position.current_action() == 'appoint'


@rules.predicate
def can_set_applicant(user, position):
    return position.role.role_type in Role.edit_applicant_role_types(user)


@rules.predicate
def can_modify_position(user, position):
    return can_modify_role(user, position.role)


# Role predicates
@rules.predicate
def can_modify_role(user, role):
    return role.role_type in Role.editable_role_types(user)


@rules.predicate
def member_of_team_role(user, role):
    return not user.is_anonymous and \
      user.teams.filter(pk__in=role.teams.values_list('pk', flat=True))


# Team predicates
@rules.predicate
def member_of_team(user, team):
    return not user.is_anonymous and user.teams.filter(pk=team.pk).exists()


# Permissions
rules.add_perm('involvement', rules.always_allow)

rules.add_perm('involvement.list_contactcard', is_super | has_role_perm)
rules.add_perm('involvement.add_contactcard', is_super | has_role_perm)
rules.add_perm('involvement.change_contactcard', is_super
               | member_of_team_contactcard & can_modify_contactcard)
rules.add_perm('involvement.delete_contactcard', is_super
               | member_of_team_contactcard
               & can_modify_contactcard)

rules.add_perm('involvement.list_application', is_super | has_role_perm)
rules.add_perm('involvement.add_application', is_super | has_role_perm)
rules.add_perm('involvement.inspect_application', is_super | has_role_perm)
rules.add_perm('involvement.change_application', is_super
               | member_of_team_appl & can_modify_application)
rules.add_perm('involvement.delete_application', is_super
               | member_of_team_appl & can_modify_application)

rules.add_perm('involvement.list_position', is_super | has_role_perm)
rules.add_perm('involvement.add_position', is_super | has_role_perm)

# Fum and Board may edit for all teams
rules.add_perm('involvement.inspect_position', is_super
               | has_role_perm
               & (member_of_team_position | is_fum | is_board))
rules.add_perm('involvement.change_position', is_super
               | can_modify_position
               & (member_of_team_position | is_fum | is_board))
rules.add_perm('involvement.delete_position', is_super
               | (can_modify_position
                  & (member_of_team_position | is_fum | is_board)))

rules.add_perm('involvement.approve_position', is_super
               | (member_of_team_position & is_action_approve
                  & can_modify_position))
rules.add_perm('involvement.appoint_position', is_super
               | (member_of_team_position & is_action_appoint
                  & ~is_fum & can_set_applicant))

rules.add_perm('involvement.list_role', is_super | has_role_perm)
rules.add_perm('involvement.add_role', is_super | has_role_perm)

# Fum and Board may edit for all teams
rules.add_perm('involvement.inspect_role', is_super
               | can_modify_role & (member_of_team_role | is_fum | is_board))
rules.add_perm('involvement.change_role', is_super
               | can_modify_role & (member_of_team_role | is_fum | is_board))
rules.add_perm('involvement.delete_role', is_super
               | can_modify_role & (member_of_team_role | is_fum | is_board))

rules.add_perm('involvement.list_team', is_super | is_admin)
rules.add_perm('involvement.add_team', is_super | is_admin)
rules.add_perm('involvement.inspect_team', is_super
               | member_of_team & is_admin)
rules.add_perm('involvement.change_team', is_super
               | member_of_team & is_admin)
rules.add_perm('involvement.delete_team', is_super
               | member_of_team & is_admin)
