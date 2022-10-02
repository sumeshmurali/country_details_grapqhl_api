from mongoengine import ValidationError


def validate_string(string: str):
    if not string or not isinstance(string, str) or string.isnumeric():
        raise ValidationError(f"Expected string, Got - {string}")


def validate_coordinates(coords):
    if not isinstance(coords[0], (float, int)):
        raise ValidationError(f"Expected numeric coordinates, got - {coords}")
    if not isinstance(coords[1], (float, int)):
        raise ValidationError(f"Expected numeric coordinates, got - {coords}")

    if not -90 <= coords[1] <= 90:
        raise ValidationError(f"Latitude should be in between -90 -> 90, got - {coords[0]}")
    if not -180 <= coords[0] <= 180:
        raise ValidationError(f"Longitude should be in between -180 -> 180, got - {coords[1]}")


def validate_boolean_values(value):
    if not isinstance(value, bool):
        raise ValidationError(f"Expected True of False, got - {value}")


def validate_numbers(value):
    if type(value) not in {int, float}:
        raise ValidationError(f"Expected a number, got {value}")
