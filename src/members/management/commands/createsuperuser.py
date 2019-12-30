from django.contrib.auth.management.commands import createsuperuser
from members.models import Member


class Command(createsuperuser.Command):
    def get_input_data(self, field, message, default=None):
        if field.name == "melos_id":
            melos_id = None
            while melos_id is None:
                ssn = input("Personnummer: ")
                found_user, found_melos_id = Member.find_by_ssn(ssn)
                if found_user is None:
                    melos_id = found_melos_id
                else:
                    self.stderr.write(
                        "An account with that personnummer already exists"
                    )
                    melos_id = None

            return melos_id
        else:
            return super().get_input_data(field, message, default)
