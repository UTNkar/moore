from django.test import TestCase
from utils.validators import SSNValidator
from django.core.exceptions import ValidationError


class SSNValidatorTests(TestCase):
    def ssn_is_valid(self, ssn):
        try:
            SSNValidator()(ssn)
            return True
        except ValidationError:
            return False

    def test_long_format_with_dash(self):
        self.assertTrue(
            self.ssn_is_valid("19330524-8585"),
            "Valid SSN format failed"
        )
        self.assertTrue(
            self.ssn_is_valid("19330524-T585"),
            "Valid SSN format with T failed"
        )

    def test_long_format_with_no_dash(self):
        self.assertTrue(
            self.ssn_is_valid("193305248585"),
            "Valid SSN format failed"
        )
        self.assertTrue(
            self.ssn_is_valid("19330524T585"),
            "Valid SSN format with T failed"
        )

    def test_short_format_with_dash(self):
        self.assertTrue(
            self.ssn_is_valid("330524-8585"),
            "Valid SSN format failed"
        )
        self.assertTrue(
            self.ssn_is_valid("330524-T585"),
            "Valid SSN format with T failed"
        )

    def test_short_format_with_no_dash(self):
        self.assertTrue(
            self.ssn_is_valid("3305248585"),
            "Valid SSN format failed"
        )
        self.assertTrue(
            self.ssn_is_valid("330524T585"),
            "Valid SSN format with T failed"
        )
