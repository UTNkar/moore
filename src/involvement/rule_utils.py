import rules


@rules.predicate
def has_permission(permissions, permission_filter):
    if len(permission_filter) > 0:
        return permissions.filter(codename__in=permission_filter).exists()
    return False


@rules.predicate
def is_admin(user):
    return user.has_perm('involvement.admin')


@rules.predicate
def is_fum(user):
    return user.has_perm('involvement.fum')


@rules.predicate
def is_board(user):
    return user.has_perm('involvement.board')


@rules.predicate
def is_presidium(user):
    return user.has_perm('involvement.presidium')


@rules.predicate
def is_group_leader(user):
    return user.has_perm('involvement.group_leader')


@rules.predicate
def is_engaged(user):
    return user.has_perm('involvement.engaged')


@rules.predicate
def has_role_perm(user):
    return is_fum(user) \
        | is_board(user) \
        | is_presidium(user) \
        | is_group_leader(user)
