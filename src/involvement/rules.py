import rules
from involvement.models import Role
from involvement.rule_utils import is_admin, is_fum, has_permission, \
            has_role_perm


# Application predicates
@rules.predicate
def can_modify_application(user, application):
    return can_set_applicant(user, application.position)


# Position predicates
@rules.predicate
def is_action_approve(user, position):
    return position.current_action() == 'approve'


@rules.predicate
def is_action_appoint(user, position):
    return position.current_action() == 'appoint'


@rules.predicate
def can_set_applicant(user, position):
    permission_filter = Role.edit_applicant_codenames(user)
    return has_permission(position.role.group.permissions, permission_filter)


@rules.predicate
def can_modify_position(user, position):
    return can_modify_role(user, position.role)


# Role predicates
@rules.predicate
def can_modify_role(user, role):
    permission_filter = Role.editable_codenames(user)
    return has_permission(role.group.permissions, permission_filter)


# Permissions
rules.add_perm('involvement', rules.always_allow)

rules.add_perm('involvement.list_application', is_admin | has_role_perm)
rules.add_perm('involvement.add_application', is_admin | has_role_perm)
rules.add_perm('involvement.change_application', is_admin
               | can_modify_application)
rules.add_perm('involvement.delete_application', is_admin
               | can_modify_application)

rules.add_perm('involvement.list_position', is_admin | has_role_perm)
rules.add_perm('involvement.inspect_position', is_admin | has_role_perm)
rules.add_perm('involvement.add_position', is_admin | has_role_perm)
rules.add_perm('involvement.change_position', is_admin | can_modify_position)
rules.add_perm('involvement.delete_position', is_admin | can_modify_position)

rules.add_perm('involvement.approve_position', is_admin
               | (is_action_approve & can_modify_position))
rules.add_perm('involvement.appoint_position', is_admin
               | (is_action_appoint & ~is_fum & can_set_applicant))

rules.add_perm('involvement.list_role', is_admin | has_role_perm)
rules.add_perm('involvement.add_role', is_admin | has_role_perm)
rules.add_perm('involvement.change_role', is_admin | can_modify_role)
rules.add_perm('involvement.delete_role', is_admin | can_modify_role)

rules.add_perm('involvement.list_team', is_admin)
rules.add_perm('involvement.inspect_team', is_admin)
rules.add_perm('involvement.add_team', is_admin)
rules.add_perm('involvement.change_team', is_admin)
rules.add_perm('involvement.delete_team', is_admin)
