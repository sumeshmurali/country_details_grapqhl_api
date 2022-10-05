from mongoengine import ValidationError


def validate_string(string: str):
    """
    Validates a string
    :param string:
    :raises ValidationError if invalid coordinate:
    """
    if not string or not isinstance(string, str) or string.isnumeric():
        raise ValidationError(f"Expected string, Got - {string}")


def validate_coordinates(coords):
    """
    Checks if a coordinate is a valid one or not.
    :param coords:
    :raises ValidationError if invalid coordinate:
    """
    if not isinstance(coords[0], (float, int)):
        raise ValidationError(f"Expected numeric coordinates, got - {coords}")
    if not isinstance(coords[1], (float, int)):
        raise ValidationError(f"Expected numeric coordinates, got - {coords}")

    if not -90 <= coords[1] <= 90:
        raise ValidationError(
            f"Latitude should be in between -90 -> 90, got - {coords[0]}"
        )
    if not -180 <= coords[0] <= 180:
        raise ValidationError(
            f"Longitude should be in between -180 -> 180, got - {coords[1]}"
        )


def validate_boolean_values(value):
    """
    Validates boolean values
    :param value:
    :raises ValidationError if invalid coordinate:
    """
    if not isinstance(value, bool):
        raise ValidationError(f"Expected True of False, got - {value}")


def validate_numbers(value):
    """
    Validate numerical values
    :param value:
    :raises ValidationError if invalid coordinate:
    """
    if type(value) not in {int, float}:
        raise ValidationError(f"Expected a number, got {value}")
