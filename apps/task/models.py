from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.user.models import User
from .generator import generate_csv

COLUMN_TYPES = [
    ("name", _("Full name")),
    ("job", _("Job")),
    ("email", _("E-mail")),
    ("domain", _("Domain name")),
    ("phone", _("Phone number")),
    ("company", _("Company")),
    ("text", _("Text")),
    ("int", _("Integer")),
    ("address", _("Address")),
    ("date", _("Date")),
]

TASK_STATUSES = [
    (1, _("Error")),
    (5, _("In process")),
    (10, _("Completed")),
]

SEPARATORS = [
    (";", _(";")),
    (",", _(",")),
    ("|", _("|")),
]


class Schema(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=255)
    separator = models.CharField(_('Separator'), max_length=1, choices=SEPARATORS, default=';')
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Schema')
        verbose_name_plural = _('Schemas')


class Column(models.Model):
    schema = models.ForeignKey(Schema, verbose_name=_('Schema'), on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=255)
    start = models.IntegerField(_("From"), null=True, blank=True)
    end = models.IntegerField(_("To"), null=True, blank=True)
    kind = models.CharField(_('Column type'), max_length=16, choices=COLUMN_TYPES)
    order = models.IntegerField(_("Order"), default=1)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _('Schema')
        verbose_name_plural = _('Schemas')


class Task(models.Model):
    schema = models.ForeignKey(Schema, verbose_name=_('Schema'), on_delete=models.CASCADE)
    rows = models.IntegerField(_("Rows"), null=True, blank=True)
    status = models.IntegerField(_('Status'), choices=TASK_STATUSES, default=5)
    file = models.FileField(_('File'), null=True, blank=True)
    error = models.TextField(_("Error"), null=True, blank=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return '%s (%s)' % (self.schema.name, self.created_at.__str__)

    def save(self, *args, **kwargs):
        generate = False
        if not self.pk:
            generate = True

        super().save(*args, **kwargs)
        if generate:
            generate_csv.delay(self.pk)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Schema')
        verbose_name_plural = _('Schemas')
