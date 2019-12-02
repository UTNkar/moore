# Messages that normally isn't found using makemessages can be added here
# to force Django to detect them


def _(s):
    return s


django_standard_messages_to_add = [
    _("Username or SSN (YYYYMMDD-XXXX)"),
]
