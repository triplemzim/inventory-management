from django_registration.forms import RegistrationForm
from users.models import CustomUser

class CustomUserForm(RegistrationForm):
    django_registration_disallowed = ''
    class Meta(RegistrationForm.Meta):
        model = CustomUser