import os


class ValidationException(Exception):
    pass


def get_parameter(name: str, mandatory: bool = True):
    value = os.environ.get(name, None)
    if mandatory and value is None:
            raise ValidationException(f"Environment variable {name} not defined")
    
    if value is not None:
        if (value.startswith('http://') or value.startswith('https://')) and value.endswith('/'):
            value = value.rstrip('/')
    return value
