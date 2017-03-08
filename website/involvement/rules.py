from datetime import date

import rules

from involvement.models import Application


# General Predicates
@rules.predicate
def is_admin(user):
    return user.has_perm('involvement.admin')


@rules.predicate
def is_official(user):
    return Application.objects.filter(
        applicant=user,
        status='appointed',
        position__term_from__lte=date.today(),
        position__term_to__gte=date.today(),
        position__function__official=True,
        position__function__team_id__isnull=False,
    ).exists()


# Team Permissions
@rules.predicate
def is_team_official(user, team):
    return Application.objects.filter(
        applicant=user,
        status='appointed',
        position__term_from__lte=date.today(),
        position__term_to__gte=date.today(),
        position__function__official=True,
        position__function__team=team,
    ).exists()


# Function Predicates
@rules.predicate
def is_function_official(user, function):
    return is_team_official(user, function.team)


# Position Predicates
@rules.predicate
def is_position_official(user, position):
    return is_team_official(user, position.function.team)


@rules.predicate
def before_commencement(user, position):
    return date.today() < position.commencement


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

rules.add_perm('involvement.list_function', is_admin | is_official)
rules.add_perm('involvement.add_function', is_admin | is_official)
rules.add_perm('involvement.change_function', is_admin | is_function_official)
rules.add_perm('involvement.delete_function', is_admin)

rules.add_perm('involvement.list_position', is_admin | is_official)
rules.add_perm('involvement.add_position', is_admin | is_official)
rules.add_perm('involvement.change_position', is_admin | is_position_official)
rules.add_perm('involvement.delete_position', is_admin
               | (is_position_official & before_commencement))

rules.add_perm('involvement.list_application', is_admin)
rules.add_perm('involvement.add_application', is_admin | is_official)
rules.add_perm('involvement.change_application', is_admin | is_applicant)
rules.add_perm('involvement.delete_application', is_admin
               | (is_applicant & ~is_past_due))
