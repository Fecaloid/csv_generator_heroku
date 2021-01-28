from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    first_name = False
    last_name = False
    email = False

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    @staticmethod
    def _create_user(username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = User.objects.create(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
