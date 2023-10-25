################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2009-2022  Hybird
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

from __future__ import annotations

from typing import Any, Iterator

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...creme_core.models import fields as core_fields
from ...creme_core.models import CremeEntity, CremeModel, FieldsConfig
from ...creme_core.common.utils import COUNTRIES

class AbstractAddress(CremeModel):
    name = models.CharField(_('Name'), max_length=100, blank=True)
    address = models.TextField(_('Address'), max_length=255, blank=True, default="")
    po_box = models.CharField(
        _('PO box'), max_length=50, blank=True,
    ).set_tags(optional=True)
    zipcode = models.CharField(
        _('Post/Zip-code'), max_length=100, blank=True,
    ).set_tags(optional=True)
    street = models.CharField(_("Street"), max_length=100, blank=True, default="").set_tags(optional=True)
    city = models.CharField(
        _('City'), max_length=100, blank=True,
    ).set_tags(optional=True)
    department = models.CharField(
        _('Department'), max_length=100, blank=True,
    ).set_tags(optional=True)
    state = models.CharField(
        _('State'), max_length=100, blank=True,
    ).set_tags(optional=True)
    country = models.CharField(
        _('Country'), max_length=40, choices=COUNTRIES, blank=True, default=""
    ).set_tags(optional=True)
    content_type = core_fields.EntityCTypeForeignKey(
        related_name='+', editable=False,
    ).set_tags(viewable=False)
    object = models.ForeignKey(
        CremeEntity, related_name='persons_addresses',
        editable=False, on_delete=models.CASCADE,
    ).set_tags(viewable=False)
    owner = core_fields.RealEntityForeignKey(ct_field='content_type', fk_field='object')

    creation_label = _('Create an address')
    save_label     = _('Save the address')

    STR_FIELD_NAMES: list[list[str]] = [
        ['address', 'zipcode', 'city', 'department'],
        ['po_box', 'state', 'country'],
    ]
    STR_SEPARATOR = ' '

    class Meta(CremeModel.Meta):
        abstract = True
        app_label = 'persons'
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ('id',)

    def __str__(self):
        s = ''
        join = self.STR_SEPARATOR.join
        allowed_fnames = {*self.info_field_names()}

        def field_value(fname):
            return getattr(self, fname) if fname in allowed_fnames else None

        for field_names in self.STR_FIELD_NAMES:
            s = join(filter(None, (field_value(fn) for fn in field_names)))

            if s:
                break

        return self.city if self.city else s

    def get_complete_address(self):
        address = ""
        if self.address_line:
            address += self.address_line
        if self.street:
            if address:
                address += ", " + self.street
            else:
                address += self.street
        if self.city:
            if address:
                address += ", " + self.city
            else:
                address += self.city
        if self.state:
            if address:
                address += ", " + self.state
            else:
                address += self.state
        if self.postcode:
            if address:
                address += ", " + self.postcode
            else:
                address += self.postcode
        if self.country:
            if address:
                address += ", " + self.get_country_display()
            else:
                address += self.get_country_display()
        return address

    def get_edit_absolute_url(self):
        return reverse('persons__edit_address', args=(self.id,))

    def get_related_entity(self):  # For generic views
        return self.owner

    def __bool__(self):  # Used by forms to detect empty addresses
        return any(fvalue for fname, fvalue in self.info_fields)

    def clone(self, entity):
        """Returns a new cloned (saved) address for a (saved) entity."""
        return type(self).objects.create(owner=entity, **dict(self.info_fields))

    @classmethod
    def info_field_names(cls) -> tuple[str, ...]:
        is_field_hidden = FieldsConfig.objects.get_for_model(cls).is_field_hidden
        excluded = {'id', 'content_type', 'object'}  # TODO: just exclude not viewable ?
        return tuple(
            f.name
            for f in cls._meta.fields
            if f.name not in excluded and not is_field_hidden(f)
        )

    @property
    def info_fields(self) -> Iterator[tuple[str, Any]]:
        for fname in self.info_field_names():
            yield fname, getattr(self, fname)


class Address(AbstractAddress):
    class Meta(AbstractAddress.Meta):
        swappable = 'PERSONS_ADDRESS_MODEL'
