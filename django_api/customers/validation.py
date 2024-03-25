from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class CustomEmailValidator(EmailValidator):
    def __init__(self, *args, **kwargs):
        self.allowlist = kwargs.pop('allowlist', [])
        super().__init__(*args, **kwargs)

    def __call__(self, value):
        super().__call__(value)
        user_part, domain_part = value.rsplit('@', 1)
        if domain_part not in self.allowlist:
            raise ValidationError(self.message, code=self.code)
