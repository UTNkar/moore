from datetime import date

import rules

from involvement.models import official_of, member_of, Position


# General Predicates
@rules.predicate
def is_admin(user):
    return user.has_perm('involvement.admin')


@rules.predicate
def is_official(user):
    return len(official_of(user)) > 0


@rules.predicate
def is_approval_committee(user):
    return Position.objects.filter(
        approval_committee__in=member_of(user)
    ).exists()


# Team Permissions
@rules.predicate
def is_team_official(user, team):
    return team in official_of(user)


# Role Predicates
@rules.predicate
def is_role_official(user, role):
    return is_team_official(user, role.team)


# Position Predicates
@rules.predicate
def is_position_official(user, position):
    return is_team_official(user, position.role.team)


@rules.predicate
def before_recruitment_start(user, position):
    return date.today() < position.recruitment_start


@rules.predicate
def approve_state(user, position):
    return position.current_action() == 'approve'


@rules.predicate
def is_approval_committee_for(user, position):
    if position.approval_committee is None:
        return False
    else:
        return position.approval_committee in member_of(user)


@rules.predicate
def appoint_state(user, position):
    return position.current_action() == 'appoint'


# Application Predicates
@rules.predicate
def is_applicant(user, application):
    return application.applicant == user


@rules.predicate
def is_past_due(user, application):
    return application.position.is_past_due()


# Permissions
rules.add_perm('involvement', rules.always_allow)

rules.add_perm('involvement.list_team', is_admin | is_official)
rules.add_perm('involvement.add_team', is_admin)
rules.add_perm('involvement.change_team', is_admin | is_team_official)
rules.add_perm('involvement.delete_team', is_admin)

rules.add_perm('involvement.list_role', is_admin | is_official)
rules.add_perm('involvement.add_role', is_admin | is_official)
rules.add_perm('involvement.change_role', is_admin | is_role_official)
rules.add_perm('involvement.delete_role', is_admin)

rules.add_perm('involvement.list_position', is_admin | is_official
               | is_approval_committee)
rules.add_perm('involvement.add_position', is_admin | is_official)
rules.add_perm('involvement.change_position', is_admin | is_position_official)
rules.add_perm('involvement.approve_position', is_admin
               | (is_approval_committee_for & approve_state))
rules.add_perm('involvement.appoint_position', is_admin
               | (is_position_official & appoint_state))
rules.add_perm('involvement.delete_position', is_admin
               | (is_position_official & before_recruitment_start))

rules.add_perm('involvement.list_application', is_admin)
rules.add_perm('involvement.add_application', is_admin | is_official)
rules.add_perm('involvement.change_application', is_admin | is_applicant)
rules.add_perm('involvement.delete_application', is_admin
               | (is_applicant & ~is_past_due))
