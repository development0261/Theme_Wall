from django.core.exceptions import ValidationError


def file_size(value):
    filesize = value.size
    if filesize>10485760:
        raise ValidationError("maximum Video file size is 10mb")
    else:
        return value