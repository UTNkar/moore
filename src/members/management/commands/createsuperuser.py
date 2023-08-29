from django.contrib.auth.management.commands import createsuperuser
from members.models import Member


class Command(createsuperuser.Command):
    """Extends the built-in createsuperuser command"""
    def get_input_data(self, field, message, default=None):
        """
            Extends get_input_data from the build in createsuperuser
            so that we can get a unicore id for the superuser to be
            created.
        """
        if field.name == "unicore_id":
            unicore_id = None
            while unicore_id is None:
                ssn = input("Personnummer: ")
                found_user, found_unicore_id = Member.find_by_ssn(ssn)
                if found_user is None:
                    unicore_id = found_unicore_id
                else:
                    self.stderr.write(
                        "An account with that personnummer already exists"
                    )
                    unicore_id = None

            return unicore_id
        else:
            return super().get_input_data(field, message, default)
