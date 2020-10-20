from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from djmoney.models.validators import MinMoneyValidator
from django.contrib.gis.db import models as gis_models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from phone_field import PhoneField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum, Q
from vies.models import VATINField
from simple_history.models import HistoricalRecords
import decimal
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
import django_futils.utils as utils
import django_futils.constants as const


################
# BasicElement #
################
class BasicElement(models.Model):
    code = models.CharField(_('code'),
                            max_length=const.CODE_LENGTH,
                            unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


################
# Type classes #
################
class Type(BasicElement):
    type = models.CharField(_('type'),
                            max_length=const.NAME_LENGTH,
                            db_index=True)

    def __str__(self):
        return self.type

    class Meta:
        abstract = True


class AddressType(Type):
    class Meta:
        abstract = True
        verbose_name = _('address type')
        verbose_name_plural = _('address types')


class EmailType(Type):
    class Meta:
        abstract = True
        verbose_name = _('email type')
        verbose_name_plural = _('email types')


class TelephoneType(Type):
    class Meta:
        abstract = True
        verbose_name = _('telephone type')
        verbose_name_plural = _('telephone types')


class AttachmentType(Type):
    class Meta:
        abstract = True
        verbose_name = _('attachment type')
        verbose_name_plural = _('attachment types')


###################
# Element classes #
###################
class Element(BasicElement):
    name = models.CharField(_('name'),
                            max_length=const.NAME_LENGTH,
                            db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Municipality(Element):
    r"""This is the equivalent of:
        'comune'    in 'IT'
    """
    country = CountryField(_('country'), default='IT')

    class Meta:
        abstract = True
        verbose_name = _('municipality')
        verbose_name_plural = _('municipalities')


class RecordTimestamps(models.Model):
    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


##################
# Normal classes #
##################
class CommonAttachment(RecordTimestamps):
    name = models.CharField(_('name'), max_length=const.NAME_LENGTH)
    notes = models.TextField(_('notes'), blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class HasPrimary(RecordTimestamps):
    is_primary = models.BooleanField(_('is primary'), default=False)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if self.is_primary:
            raise ValidationError(_('cannot delete primary object'))
        else:
            super().delete(*args, **kwargs)


class TelephoneCommon(HasPrimary):
    number = PhoneField(_('number'), unique=True, db_index=True)
    has_whatsapp = models.BooleanField(_('has whatsapp'), default=False)
    has_telegram = models.BooleanField(_('has telegram'), default=False)
    is_primary = models.BooleanField(_('primary'), default=False)

    def __str__(self):
        return str(self.number)

    class Meta:
        abstract = True


class PersonTelephone(TelephoneCommon):
    class Meta:
        abstract = True
        constraints = [
            # This constraint should nevery be hit because of the save method
            # which corrects the error.
            models.UniqueConstraint(
                fields=['person'],
                condition=Q(is_primary=True),
                name='is_primary_persontelephone_costraint'),
            models.UniqueConstraint(
                fields=['number', 'type', 'person'],
                name='persontelephone_constraint'),
        ]
        verbose_name = _('person\'s telephone')
        verbose_name_plural = _('peoples\' telephone')

    def save(self, *args, **kwargs):
        # One object must always be primary.
        try:
            telephone = PersonTelephone.objects.get(
                Q(person=self.person) & Q(is_primary=True))
            if self.is_primary:
                # Change value on the fly.
                PersonTelephone.objects.filter(
                    Q(id=telephone.id)).update(is_primary=False)
                self.is_primary = True
        except ObjectDoesNotExist:
            self.is_primary = True

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if PersonTelephone.objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary telephone to a different person once it is set'))


class CompanyTelephone(TelephoneCommon):
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['company'],
                condition=Q(is_primary=True),
                name='is_primary_companytelephone_costraint'),
            models.UniqueConstraint(
                fields=['number', 'type', 'company'],
                name='companytelephone_constraint'),
        ]

        verbose_name = _('company\'s telephone')
        verbose_name_plural = _('companies\' telephone')

    def save(self, *args, **kwargs):
        # One object must always be primary.
        try:
            telephone = CompanyTelephone.objects.get(
                Q(company=self.company) & Q(is_primary=True))
            if self.is_primary:
                # Change value on the fly.
                CompanyTelephone.objects.filter(
                    Q(id=telephone.id)).update(is_primary=False)
                self.is_primary = True
        except ObjectDoesNotExist:
            self.is_primary = True

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if CompanyTelephone.objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary telephone to a different company once it is set'))


class EmailCommon(HasPrimary):
    email = models.EmailField(_('email'),
                              max_length=const.EMAIL_MAX_LENGTH,
                              unique=True,
                              db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.email)


class PersonEmail(EmailCommon):
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['person'],
                                    condition=Q(is_primary=True),
                                    name='is_primary_personemail_costraint'),
            models.UniqueConstraint(
                fields=['email', 'type', 'person'],
                name='personemail_constraint'),
        ]
        verbose_name = _('person\'s email')
        verbose_name_plural = _('peoples\' email')

    def save(self, *args, **kwargs):
        # One object must always be primary.
        try:
            email = PersonEmail.objects.get(
                Q(person=self.person) & Q(is_primary=True))
            if self.is_primary:
                # Change value on the fly.
                PersonEmail.objects.filter(
                    Q(id=email.id)).update(is_primary=False)
                self.is_primary = True
        except ObjectDoesNotExist:
            self.is_primary = True

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if PersonEmail.objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary email to a different person once it is set'))


class CompanyEmail(EmailCommon):
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['company'],
                                    condition=Q(is_primary=True),
                                    name='is_primary_companyemail_costraint'),
            models.UniqueConstraint(
                fields=['email', 'type', 'company'],
                name='companyemail_constraint'),
        ]
        verbose_name = _('company\'s email')
        verbose_name_plural = _('companies\' email')

    def save(self, *args, **kwargs):
        # One object must always be primary.
        try:
            email = CompanyEmail.objects.get(
                Q(company=self.company) & Q(is_primary=True))
            if self.is_primary:
                # Change value on the fly.
                CompanyEmail.objects.filter(
                    Q(id=email.id)).update(is_primary=False)
                self.is_primary = True
        except ObjectDoesNotExist:
            self.is_primary = True

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if CompanyEmail.objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary email to a different company once it is set'))


class AddressCommon(HasPrimary):
    map = gis_models.PointField(_('map'), blank=True, null=True)
    street_number = models.CharField(_('street number'),
                                     max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                     db_index=True)
    street = models.CharField(_('street'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    city = models.CharField(_('city'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    postal_code = models.CharField(_('postal code'),
                                   max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                   blank=True)
    auto_fill = models.BooleanField(_('auto fill'), default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.point, self.postal_code = utils.get_address_data(
            self.municipality.country.code, self.city, self.street_number,
            self.street, self.postal_code, self.auto_fill)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.street + ', ' + self.street_number + ', ' + self.city


class PersonAddress(AddressCommon):
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['person'],
                                    condition=Q(is_primary=True),
                                    name='is_primary_presonaddress_constraint'),
            # See
            # https://stackoverflow.com/questions/55044802/django-admin-inline-unique-constraint-violation-on-edit
            # https://stackoverflow.com/questions/40891574/how-can-i-set-a-table-constraint-deferrable-initially-deferred-in-django-model
            # https://docs.djangoproject.com/en/3.1/ref/models/constraints/#deferrable
            models.UniqueConstraint(
                fields=['street_number', 'street', 'city', 'municipality', 'type', 'person'],
                name='personaddress_constraint'),
        ]
        verbose_name = _('person\'s address')
        verbose_name_plural = _('peoples\' address')

    def save(self, *args, **kwargs):
        # One object must always be primary.
        try:
            address = PersonAddress.objects.get(
                Q(person=self.person) & Q(is_primary=True))
            if self.is_primary:
                # Change value on the fly.
                PersonAddress.objects.filter(
                    Q(id=address.id)).update(is_primary=False)
                self.is_primary = True
        except ObjectDoesNotExist:
            self.is_primary = True

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if PersonAddress.objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary address to a different person once it is set'))


class CompanyAddress(AddressCommon):
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['company'],
                condition=Q(is_primary=True),
                name='is_primary_companyaddress_costraint'),
            models.UniqueConstraint(
                fields=['street_number', 'street', 'city', 'municipality', 'type', 'company'],
                name='companyaddress_constraint'),
        ]
        verbose_name = _('company\'s address')
        verbose_name_plural = _('companies\' address')

    def save(self, *args, **kwargs):
        # One object must always be primary.
        try:
            address = CompanyAddress.objects.get(
                Q(company=self.company) & Q(is_primary=True))
            if self.is_primary:
                # Change value on the fly.
                CompanyAddress.objects.filter(
                    Q(id=address.id)).update(is_primary=False)
                self.is_primary = True
        except ObjectDoesNotExist:
            self.is_primary = True

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if CompanyAddress.objects.get(pk=self.pk).company != self.company:
                raise ValidationError(_('cannot assign a primary address to a different company once it is set'))


class Company(RecordTimestamps):
    name = models.CharField(_('name'), max_length=const.GENERIC_CHAR_FIELD_LENGTH)
    vat = VATINField(_('VAT'), unique=True)
    is_primary = models.BooleanField(_('is primary'), default=False)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['person'],
                                    condition=Q(is_primary=True),
                                    name='is_primary_company_costraint')
        ]
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def save(self, *args, **kwargs):
        # One object must always be primary.
        try:
            company = Company.objects.get(
                Q(person=self.person) & Q(is_primary=True))
            if self.is_primary:
                # Change value on the fly.
                Company.objects.filter(
                    Q(id=company.id)).update(is_primary=False)
                self.is_primary = True
        except ObjectDoesNotExist:
            self.is_primary = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Person(RecordTimestamps):
    first_name = models.CharField(_('first name'),
                                  max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                  db_index=True)
    last_name = models.CharField(_('last name'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    date_of_birth = models.DateField(_('date of birth'), default=timezone.now)
    city_of_birth = models.CharField(_('city of birth'), max_length=const.GENERIC_CHAR_FIELD_LENGTH)
    fiscal_code = models.CharField(_('fiscal code'),
                                   max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                   unique=True,
                                   db_index=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + '[' + self.fiscal_code + ']'

    class Meta:
        abstract = True
        verbose_name = _('person')
        verbose_name_plural = _('people')


class PersonAttachment(CommonAttachment):
    file = models.FileField(_('file'),
                            upload_to=utils.personattachment_directory_path,
                            null=True)

    class Meta:
        abstract = True
        verbose_name = _('person attachment')
        verbose_name_plural = _('person attachments')


class NominatimCache(RecordTimestamps):
    r"""As required by the terms of use, Nominatim results must be cached.
        See
        https://operations.osmfoundation.org/policies/nominatim/
    """
    request_url = models.URLField(_('request url'), max_length=16384, db_index=True)
    postal_code = models.CharField(_('postal code'),
                                   max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                   blank=True)
    map = gis_models.PointField(_('map'), blank=True, null=True)
    cache_hits = models.IntegerField(_('cache hits'), default=0)

    class Meta:
        abstract = True
        verbose_name = _('Nominatim cache')
        verbose_name_plural = _('Nominatim caches')
