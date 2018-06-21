import rules


@rules.predicate
def is_super(user):
    return user.is_superuser


@rules.predicate
def is_admin(user):
    return not user.is_anonymous and \
        user.roles.filter(role_type='admin').exists()


@rules.predicate
def is_fum(user):
    return not user.is_anonymous and \
        user.roles.filter(role_type='fum').exists()


@rules.predicate
def is_board(user):
    return not user.is_anonymous and \
        user.roles.filter(role_type='board').exists()


@rules.predicate
def is_presidium(user):
    return not user.is_anonymous and \
        user.roles.filter(role_type='presidium').exists()


@rules.predicate
def is_group_leader(user):
    return not user.is_anonymous and \
        user.roles.filter(role_type='group_leader').exists()


@rules.predicate
def is_engaged(user):
    return not user.is_anonymous and \
        user.roles.filter(role_type='engaged').exists()


@rules.predicate
def has_role_perm(user):
    return not user.is_anonymous and \
        user.roles.exclude(role_type='engaged').exists()
