import rules
from datetime import date
from involvement.models import Team, Position, CurrentMandate


# General Predicates
@rules.predicate
def is_admin(user):
    return user.has_perm('involvement.admin')


@rules.predicate
def has_team_official(user):
    return len(Team.official_of(user)) > 0


@rules.predicate
def is_approval_committee(user):
    return Position.objects.filter(
        approval_committee__in=Team.member_of(user)
    ).exists()


# Team Permissions
@rules.predicate
def is_team_official(user, team):
    return team in Team.official_of(user)


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
        return position.approval_committee in Team.member_of(user)


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


@rules.predicate
def has_mandate(user):
    return CurrentMandate.objects.filter(
        applicant=user,
    ).exists()


@rules.predicate
def is_mandate(user, application):
    return CurrentMandate.objects.filter(
        applicant=user,
        position=application.position
    ).exists()


# Permissions
rules.add_perm('involvement', rules.always_allow)

rules.add_perm('involvement.list_team', is_admin | has_team_official)
rules.add_perm('involvement.inspect_team', is_admin | is_team_official)
rules.add_perm('involvement.add_team', is_admin)
rules.add_perm('involvement.change_team', is_admin | is_team_official)
rules.add_perm('involvement.delete_team', is_admin)

rules.add_perm('involvement.list_role', is_admin | has_team_official)
rules.add_perm('involvement.add_role', is_admin | has_team_official)
rules.add_perm('involvement.change_role', is_admin | is_role_official)
rules.add_perm('involvement.delete_role', is_admin)

rules.add_perm('involvement.list_position', is_admin | has_team_official
               | is_approval_committee)
rules.add_perm('involvement.inspect_position', is_admin | is_position_official
               | is_approval_committee_for)
rules.add_perm('involvement.add_position', is_admin | has_team_official)
rules.add_perm('involvement.change_position', is_admin | is_position_official)
rules.add_perm('involvement.approve_position', is_admin
               | (is_approval_committee_for & approve_state))
rules.add_perm('involvement.appoint_position', is_admin
               | (is_position_official & appoint_state))
rules.add_perm('involvement.delete_position', is_admin
               | (is_position_official & before_recruitment_start))

rules.add_perm('involvement.list_application', is_admin | has_mandate)
rules.add_perm('involvement.add_application', is_admin | is_mandate)
rules.add_perm('involvement.change_application', is_admin | is_mandate)
rules.add_perm('involvement.delete_application', is_admin | is_mandate)
