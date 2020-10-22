from django.db import models
from django.utils.translation import gettext_lazy as _

from .abstract_models import (AbstractAddressType, AbstractEmailType, AbstractTelephoneType, AbstractAttachmentType, AbstractMunicipality, AbstractPersonTelephone, AbstractCompanyTelephone,AbstractPersonEmail, AbstractCompanyEmail, AbstractPersonAddress, AbstractCompanyAddress, AbstractCompany, AbstractPerson, AbstractPersonAttachment, AbstractNominatimCache)

################
# Type classes #
################
class AddressType(AbstractAddressType):
    pass


class EmailType(AbstractEmailType):
    pass


class TelephoneType(AbstractTelephoneType):
    pass


class AttachmentType(AbstractAttachmentType):
    pass

###################
# Element classes #
###################
class Municipality(AbstractMunicipality):
    pass


class PersonTelephone(AbstractPersonTelephone):
    type = models.ForeignKey(
        'TelephoneType',
        related_name='persontelephone_of_this_telephonetype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    person = models.ForeignKey(
        'Person',
        related_name='persontelephone_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )


class CompanyTelephone(AbstractCompanyTelephone):
    type = models.ForeignKey(
        'TelephoneType',
        related_name='companytelephone_of_this_telephonetype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    company = models.ForeignKey(
        'Company',
        related_name='companytelephone_of_this_company',
        on_delete=models.CASCADE,
        verbose_name=_('company'),
    )


class PersonEmail(AbstractPersonEmail):
    type = models.ForeignKey(
        'EmailType',
        related_name='personemail_of_this_emailtype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    person = models.ForeignKey(
        'Person',
        related_name='personemail_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )


class CompanyEmail(AbstractCompanyEmail):
    type = models.ForeignKey(
        'EmailType',
        related_name='companyemail_of_this_emailtype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    company = models.ForeignKey(
        'Company',
        related_name='companyemail_of_this_company',
        on_delete=models.CASCADE,
        verbose_name=_('company'),
    )

class PersonAddress(AbstractPersonAddress):
    type = models.ForeignKey(
        'AddressType',
        related_name='personaddress_of_this_addresstype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    municipality = models.ForeignKey(
        'Municipality',
        related_name='personaddress_address_of_this_municipality',
        on_delete=models.PROTECT,
        verbose_name=_('municipality'),
    )
    person = models.ForeignKey(
        'Person',
        related_name='personaddress_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )


class CompanyAddress(AbstractCompanyAddress):
    type = models.ForeignKey(
        'AddressType',
        related_name='companyaddress_of_this_addresstype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    municipality = models.ForeignKey(
        'Municipality',
        related_name='companyaddress_of_this_municipality',
        on_delete=models.PROTECT,
        verbose_name=_('municipality'),
    )
    company = models.ForeignKey(
        'Company',
        related_name='companyaddress_of_this_company',
        on_delete=models.CASCADE,
        verbose_name=_('company'),
    )


class PersonAttachment(AbstractPersonAttachment):
    type = models.ForeignKey(
        'AttachmentType',
        related_name='personattachment_of_this_attachmenttype',
        on_delete=models.PROTECT,
        verbose_name=_('attachment type'),
    )
    person = models.ForeignKey(
        'Person',
        related_name='personattachment_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
        null=True,
        blank=True,
    )


class Person(AbstractPerson):
    pass


class Company(AbstractPerson):
    person = models.ForeignKey(
        'Person',
        related_name='company_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )


class NominatimCache(AbstractNominatimCache):
    pass
