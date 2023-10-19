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

import logging

from django.apps import apps
from django.utils.translation import gettext as _

from ..creme_core import bricks as core_bricks
from ..creme_core.core.entity_cell import EntityCellRegularField
from ..creme_core.gui.menu import ContainerEntry
from ..creme_core.management.commands.creme_populate import BasePopulator
from ..creme_core.models import (
    BrickDetailviewLocation,
    CustomFormConfigItem,
    HeaderFilter,
    MenuConfigItem,
    RelationType,
    SearchConfigItem,
)
from ..creme_core.utils import create_if_needed
from ..opportunities import get_opportunity_model
from ..persons import get_contact_model

from . import bricks, constants, custom_forms, get_event_model
from .menu import EventsEntry
from .models import EventType

logger = logging.getLogger(__name__)


class Populator(BasePopulator):
    dependencies = ['creme_core']

    def populate(self):
        already_populated = RelationType.objects.filter(
            pk=constants.REL_SUB_IS_INVITED_TO,
        ).exists()

        Event = get_event_model()
        Contact = get_contact_model()
        Opportunity = get_opportunity_model()

        create_rtype = RelationType.objects.smart_update_or_create
        create_rtype(
            (constants.REL_SUB_IS_INVITED_TO, _('is invited to the event'), [Contact]),
            (constants.REL_OBJ_IS_INVITED_TO, _('has invited'),             [Event]),
            is_internal=True,
        )
        create_rtype(
            (
                constants.REL_SUB_ACCEPTED_INVITATION,
                _('accepted the invitation to the event'),
                [Contact],
            ), (
                constants.REL_OBJ_ACCEPTED_INVITATION,
                _('prepares to receive'),
                [Event],
            ),
            is_internal=True,
        )
        create_rtype(
            (
                constants.REL_SUB_REFUSED_INVITATION,
                _('refused the invitation to the event'),
                [Contact],
            ), (
                constants.REL_OBJ_REFUSED_INVITATION,
                _('do not prepare to receive any more'),
                [Event],
            ),
            is_internal=True,
        )
        create_rtype(
            (constants.REL_SUB_CAME_EVENT, _('came to the event'), [Contact]),
            (constants.REL_OBJ_CAME_EVENT, _('received'),          [Event]),
            is_internal=True,
        )
        create_rtype(
            (constants.REL_SUB_NOT_CAME_EVENT, _('did not come to the event'), [Contact]),
            (constants.REL_OBJ_NOT_CAME_EVENT, _('did not receive'),           [Event]),
            is_internal=True,
        )
        create_rtype(
            (
                constants.REL_SUB_GEN_BY_EVENT,
                _('generated by the event'),
                [Opportunity],
            ), (
                constants.REL_OBJ_GEN_BY_EVENT,
                _('(event) has generated the opportunity'),
                [Event],
            ),
            is_internal=True,
        )

        # ---------------------------
        HeaderFilter.objects.create_if_needed(
            pk=constants.DEFAULT_HFILTER_EVENT, name=_('Event view'), model=Event,
            cells_desc=[
                (EntityCellRegularField, {'name': 'name'}),
                (EntityCellRegularField, {'name': 'type'}),
                (EntityCellRegularField, {'name': 'start_date'}),
                (EntityCellRegularField, {'name': 'end_date'}),
            ],
        )

        # ---------------------------
        CustomFormConfigItem.objects.create_if_needed(
            descriptor=custom_forms.EVENT_CREATION_CFORM,
        )
        CustomFormConfigItem.objects.create_if_needed(
            descriptor=custom_forms.EVENT_EDITION_CFORM,
        )

        # ---------------------------
        SearchConfigItem.objects.create_if_needed(
            Event, ['name', 'description', 'type__name'],
        )

        # ---------------------------
        if not already_populated:
            for i, name in enumerate(
                [_('Show'), _('Conference'), _('Breakfast'), _('Brunch')],
                start=1,
            ):
                create_if_needed(EventType, {'pk': i}, name=name)

            # ---------------------------
            menu_container = MenuConfigItem.objects.get_or_create(
                entry_id=ContainerEntry.id,
                entry_data={'label': _('Tools')},
                defaults={'order': 100},
            )[0]

            MenuConfigItem.objects.create(
                entry_id=EventsEntry.id, parent=menu_container, order=200,
            )

            # ---------------------------
            RIGHT = BrickDetailviewLocation.RIGHT

            BrickDetailviewLocation.objects.multi_create(
                defaults={'model': Event, 'zone': BrickDetailviewLocation.LEFT},
                data=[
                    {'order': 5},  # generic info block
                    {'brick': core_bricks.CustomFieldsBrick, 'order':  40},
                    {'brick': core_bricks.PropertiesBrick,   'order': 450},
                    {'brick': core_bricks.RelationsBrick,    'order': 500},

                    {'brick': bricks.ResultsBrick, 'order':  2, 'zone': RIGHT},
                    {'brick': core_bricks.HistoryBrick, 'order': 20, 'zone': RIGHT},
                ],
            )

            if apps.is_installed('creme.assistants'):
                logger.info(
                    'Assistants app is installed'
                    ' => we use the assistants blocks on detail view'
                )

                import creme.assistants.bricks as a_bricks

                BrickDetailviewLocation.objects.multi_create(
                    defaults={'model': Event, 'zone': RIGHT},
                    data=[
                        {'brick': a_bricks.TodosBrick,        'order': 100},
                        {'brick': a_bricks.MemosBrick,        'order': 200},
                        {'brick': a_bricks.AlertsBrick,       'order': 300},
                        {'brick': a_bricks.UserMessagesBrick, 'order': 400},
                    ]
                )

            if apps.is_installed('creme.documents'):
                # logger.info('Documents app is installed
                # => we use the Documents blocks on detail view')

                from creme_crm.creme.documents.bricks import LinkedDocsBrick

                BrickDetailviewLocation.objects.create_if_needed(
                    brick=LinkedDocsBrick, order=600, zone=RIGHT, model=Event,
                )
