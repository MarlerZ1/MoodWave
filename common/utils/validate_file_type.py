import magic
from django.core.exceptions import ValidationError

def validate_file_type(upload):
    # allowed_filetypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png', 'application/msword']
    allowed_filetypes = ['image/jpeg', 'image/jpg', 'image/png']
    upload.seek(0)
    validator = magic.Magic(uncompress=True, mime=True)
    file_type = validator.from_buffer(upload.read(1024))
    if file_type not in allowed_filetypes:
        raise ValidationError('Unsupported file')