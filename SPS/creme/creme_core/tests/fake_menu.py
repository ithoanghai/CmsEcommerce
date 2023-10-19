from ..gui.menu import CreationEntry, ListviewEntry
from ..models import FakeContact, FakeOrganisation


class FakeContactCreationEntry(CreationEntry):
    id = 'creme_core-create_contact'
    model = FakeContact


class FakeContactsEntry(ListviewEntry):
    id = 'creme_core-list_contact'
    model = FakeContact


class FakeOrganisationCreationEntry(CreationEntry):
    id = 'creme_core-create_organisation'
    model = FakeOrganisation


class FakeOrganisationsEntry(ListviewEntry):
    id = 'creme_core-list_organisation'
    model = FakeOrganisation
