from django.core import validators
from django.utils.translation import ugettext_lazy as _


class SSNValidator(validators.RegexValidator):
    century = r'[1-2][0|9]'  # YY-- Only allows 19-- and 20--
    decade = r'[0-9]{2}'  # --YY
    month = r'[0-1][0-9]'
    day = r'[0-3][0-9]'
    last_four = r'(T|t|[0-9])[0-9]{3}'  # Allows T-number SSN

    def __init__(self):
        regex_pattern = \
            r'^(' + self.century + r')?' + \
            self.decade + \
            self.month + \
            self.day + \
            r'(-|\+)?' + \
            self.last_four + \
            r'$'

        super(SSNValidator, self).__init__(
            regex=regex_pattern,
            message=_(
                'Use the format YYYYMMDD-XXXX, YYMMDD-XXXX, \
                YYYYMMDDXXXX, YYMMDDXXXX for your ssn.'
            )
        )
