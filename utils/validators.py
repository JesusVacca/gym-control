from re import match

class Validator:
    @staticmethod
    def validate_phone_number(value):
        return bool(match(r"^3\d{9}$", value))