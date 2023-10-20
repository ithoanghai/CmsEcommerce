################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2009-2023  Hybird
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

from ...creme_core.forms.base import CremeModelForm

from ..models import PaymentInformation


class _PaymentInformationForm(CremeModelForm):
    class Meta:
        model = PaymentInformation
        exclude = ('organisation', )

    def __init__(self, entity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entity = entity


class PaymentInformationEditionForm(_PaymentInformationForm):
    pass


class PaymentInformationCreationForm(_PaymentInformationForm):
    def save(self, *args, **kwargs):
        self.instance.organisation = self.entity
        return super().save(*args, **kwargs)