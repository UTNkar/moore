from django.core import validators
from django.utils.translation import ugettext_lazy as _


class SSNValidator(validators.RegexValidator):
    def __init__(self):
        super(SSNValidator, self).__init__(
            # This regex makes sure that the year is either 1900 or 2000
            regex=r'^[1-2][0|9][0-9]{2}[0-1][0-9][0-3][0-9][-](T|t|[0-9])[0-9]{3}$|'  # noqa: E501, YYYYMMDD-XXXX
                  r'^[1-2][0|9][0-9]{2}[0-1][0-9][0-3][0-9](T|t|[0-9])[0-9]{3}$|'  # noqa: E501, YYYYMMDDXXXX
                  r'^[0|9][0-9]{1}[0-1][0-9][0-3][0-9][-](T|t|[0-9])[0-9]{3}$|'  # noqa: E501, YYMMDD-XXXX
                  r'^[0|9][0-9]{1}[0-1][0-9][0-3][0-9](T|t|[0-9])[0-9]{3}$',  # noqa: E501, YYMMDDXXXX
            message=_(
                'Use the format YYYYMMDD-XXXX, YYMMDD-XXXX, \
                YYYYMMDDXXXX, YYMMDDXXXX for your ssn.'
            )
        )
