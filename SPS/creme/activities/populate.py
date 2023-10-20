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
from django.utils.translation import pgettext

from ..creme_core import bricks as core_bricks
from .. import persons
from ..creme_core.core.entity_cell import (
    EntityCellRegularField,
    EntityCellRelation,
)
from ..creme_core.core.entity_filter import condition_handler, operators
from ..creme_core.gui.menu import ContainerEntry
from ..creme_core.management.commands.creme_populate import BasePopulator
from ..creme_core.models.bricks import (
    BrickDetailviewLocation,
    BrickHomeLocation,
    SettingValue,
)
from ..creme_core.models.button_menu import (
    ButtonMenuItem,
)
from ..creme_core.models.custom_form import (
    CustomFormConfigItem,
)
from ..creme_core.models.entity_filter import (
    EntityFilter,
)
from ..creme_core.models.header_filter import (
    HeaderFilter,
)
from ..creme_core.models.menu import (
    MenuConfigItem,
)
from ..creme_core.models.relation import (
    RelationType,
)
from ..creme_core.models.search import (
    SearchConfigItem,
)
from ..creme_core.models.setting_value import (
    SettingValue,
)
from ..creme_core.utils import create_if_needed
from ..persons.constants import FILTER_CONTACT_ME

from . import (
    bricks,
    buttons,
    constants,
    custom_forms,
    get_activity_model,
    menu,
    setting_keys,
)
from .models import ActivitySubType, ActivityType, Status

logger = logging.getLogger(__name__)


class Populator(BasePopulator):
    dependencies = ['creme_core', 'persons']

    def populate(self):
        already_populated = RelationType.objects.filter(
            pk=constants.REL_SUB_LINKED_2_ACTIVITY,
        ).exists()

        Contact      = persons.get_contact_model()
        Organisation = persons.get_organisation_model()

        Activity = get_activity_model()

        # ---------------------------
        create_rtype = RelationType.objects.smart_update_or_create
        create_rtype(
            (constants.REL_SUB_LINKED_2_ACTIVITY, _('related to the activity')),
            (constants.REL_OBJ_LINKED_2_ACTIVITY, _('(activity) related to'),    [Activity]),
            minimal_display=(True, False),
        )
        rt_obj_activity_subject = create_rtype(
            (
                constants.REL_SUB_ACTIVITY_SUBJECT,
                _('is subject of the activity'),
                [Contact, Organisation],
            ), (
                constants.REL_OBJ_ACTIVITY_SUBJECT,
                _('(activity) has for subject'),
                [Activity],
            ),
            is_internal=True,  # NB: avoid the disabling of this RelationType
            minimal_display=(True, False),
        )[1]
        rt_obj_part_2_activity = create_rtype(
            (constants.REL_SUB_PART_2_ACTIVITY, _('participates to the activity'),  [Contact]),
            (constants.REL_OBJ_PART_2_ACTIVITY, _('(activity) has as participant'), [Activity]),
            is_internal=True,
            minimal_display=(True, False),
        )[1]

        # ---------------------------
        def create_status(pk, name):
            create_if_needed(
                Status,
                {'pk': pk},
                name=name, description=name, is_custom=False,
            )

        create_status(constants.STATUS_PLANNED,     pgettext('activities-status', 'Planned')),
        create_status(constants.STATUS_IN_PROGRESS, pgettext('activities-status', 'In progress')),
        create_status(constants.STATUS_DONE,        pgettext('activities-status', 'Done')),
        create_status(constants.STATUS_DELAYED,     pgettext('activities-status', 'Delayed')),
        create_status(constants.STATUS_CANCELLED,   pgettext('activities-status', 'Cancelled')),

        # ---------------------------
        act_types_info = {
            # constants.ACTIVITYTYPE_TASK: {
            constants.UUID_TYPE_TASK: {
                'name': _('Task'),           'day': 0, 'hour': '00:15:00',
            },
            # constants.ACTIVITYTYPE_MEETING: {
            constants.UUID_TYPE_MEETING: {
                'name': _('Meeting'),        'day': 0, 'hour': '00:15:00',
            },
            # constants.ACTIVITYTYPE_PHONECALL: {
            constants.UUID_TYPE_PHONECALL: {
                'name': _('Phone call'),     'day': 0, 'hour': '00:15:00',
            },
            # constants.ACTIVITYTYPE_GATHERING: {
            constants.UUID_TYPE_GATHERING: {
                'name': _('Gathering'),      'day': 0, 'hour': '00:15:00',
            },
            # constants.ACTIVITYTYPE_SHOW: {
            constants.UUID_TYPE_SHOW: {
                'name': _('Show'),           'day': 1, 'hour': '00:00:00',
            },
            # constants.ACTIVITYTYPE_DEMO: {
            constants.UUID_TYPE_DEMO: {
                'name': _('Demonstration'),  'day': 0, 'hour': '01:00:00',
            },
            # constants.ACTIVITYTYPE_INDISPO: {
            constants.UUID_TYPE_UNAVAILABILITY: {
                'name': _('Unavailability'), 'day': 1, 'hour': '00:00:00',
            },
        }
        act_types = {
            # pk: create_if_needed(
            #     ActivityType,
            #     {'pk': pk},
            #     name=info['name'],
            #     default_day_duration=info['day'], default_hour_duration=info['hour'],
            #     is_custom=False,
            # ) for pk, info in act_types_info.items()
            uid: create_if_needed(
                ActivityType,
                {'uuid': uid},
                name=info['name'],
                default_day_duration=info['day'], default_hour_duration=info['hour'],
                is_custom=False,
            ) for uid, info in act_types_info.items()
        }

        # def create_subtype(atype, pk, name, is_custom=False):
        #     create_if_needed(
        #         ActivitySubType,
        #         {'pk': pk},
        #         name=name, type=atype, is_custom=is_custom,
        #     )
        def update_or_create_subtype(*, atype, uid, name, is_custom=False):
            # create_if_needed(
            #     ActivitySubType,
            #     {'uuid': uid},
            #     name=name, type=atype, is_custom=is_custom,
            # )
            ActivitySubType.objects.update_or_create(
                uuid=uid,
                defaults={
                    'name': name, 'type': atype, 'is_custom': is_custom,
                }
            )

        # meeting_t = act_types[constants.ACTIVITYTYPE_MEETING]
        # for pk, name in [
        #     (constants.ACTIVITYSUBTYPE_MEETING_MEETING,       _('Meeting')),
        #     (constants.ACTIVITYSUBTYPE_MEETING_QUALIFICATION, _('Qualification')),
        #     (constants.ACTIVITYSUBTYPE_MEETING_REVIVAL,       _('Revival')),
        #     (constants.ACTIVITYSUBTYPE_MEETING_NETWORK,       _('Network')),
        #     (constants.ACTIVITYSUBTYPE_MEETING_OTHER, pgettext('activities-meeting', 'Other')),
        # ]:
        #     create_subtype(meeting_t, pk, name)
        meeting_t = act_types[constants.UUID_TYPE_MEETING]
        for uid, name in [
            (constants.UUID_SUBTYPE_MEETING_MEETING,       _('Meeting')),
            (constants.UUID_SUBTYPE_MEETING_QUALIFICATION, _('Qualification')),
            (constants.UUID_SUBTYPE_MEETING_REVIVAL,       _('Revival')),
            (constants.UUID_SUBTYPE_MEETING_NETWORK,       _('Network')),
            (constants.UUID_SUBTYPE_MEETING_OTHER, pgettext('activities-meeting', 'Other')),
        ]:
            update_or_create_subtype(atype=meeting_t, uid=uid, name=name)

        # pcall_t = act_types[constants.ACTIVITYTYPE_PHONECALL]
        # for pk, name in [
        #     (constants.ACTIVITYSUBTYPE_PHONECALL_INCOMING,   _('Incoming')),
        #     (constants.ACTIVITYSUBTYPE_PHONECALL_OUTGOING,   _('Outgoing')),
        #     (constants.ACTIVITYSUBTYPE_PHONECALL_CONFERENCE, _('Conference')),
        #     (constants.ACTIVITYSUBTYPE_PHONECALL_FAILED,     _('Outgoing - Failed')),
        # ]:
        #     create_subtype(pcall_t, pk, name)
        pcall_t = act_types[constants.UUID_TYPE_PHONECALL]
        for uid, name in [
            (constants.UUID_SUBTYPE_PHONECALL_INCOMING,   _('Incoming')),
            (constants.UUID_SUBTYPE_PHONECALL_OUTGOING,   _('Outgoing')),
            (constants.UUID_SUBTYPE_PHONECALL_CONFERENCE, _('Conference')),
            (constants.UUID_SUBTYPE_PHONECALL_FAILED,     _('Outgoing - Failed')),
        ]:
            update_or_create_subtype(atype=pcall_t, uid=uid, name=name)

        # unav_t = act_types[constants.ACTIVITYTYPE_INDISPO]
        # create_subtype(
        #     unav_t,
        #     pk=constants.ACTIVITYSUBTYPE_UNAVAILABILITY, name=_('Unavailability'),
        # )
        unav_t = act_types[constants.UUID_TYPE_UNAVAILABILITY]
        update_or_create_subtype(
            atype=unav_t, uid=constants.UUID_SUBTYPE_UNAVAILABILITY, name=_('Unavailability'),
        )

        # ---------------------------
        HeaderFilter.objects.create_if_needed(
            pk=constants.DEFAULT_HFILTER_ACTIVITY,
            name=_('Activity view'),
            model=Activity,
            cells_desc=[
                (EntityCellRegularField, {'name': 'start'}),
                (EntityCellRegularField, {'name': 'title'}),
                (EntityCellRegularField, {'name': 'type'}),
                EntityCellRelation(model=Activity, rtype=rt_obj_part_2_activity),
                EntityCellRelation(model=Activity, rtype=rt_obj_activity_subject),
                (EntityCellRegularField, {'name': 'user'}),
                (EntityCellRegularField, {'name': 'end'}),
            ],
        )

        # ---------------------------
        create_efilter = EntityFilter.objects.smart_update_or_create

        # for pk, name, atype_id in [
        #     (constants.EFILTER_MEETINGS,   _('Meetings'),    constants.ACTIVITYTYPE_MEETING),
        #     (constants.EFILTER_PHONECALLS, _('Phone calls'), constants.ACTIVITYTYPE_PHONECALL),
        #     (constants.EFILTER_TASKS,      _('Tasks'),       constants.ACTIVITYTYPE_TASK),
        # ]:
        #     create_efilter(
        #         pk, name=name, model=Activity, is_custom=False, user='admin',
        #         conditions=[
        #             condition_handler.RegularFieldConditionHandler.build_condition(
        #                 model=Activity,
        #                 operator=operators.EqualsOperator,
        #                 field_name='type',
        #                 values=[atype_id],
        #             ),
        #         ],
        #     )
        for pk, name, atype_uuid in [
            (constants.EFILTER_MEETINGS,   _('Meetings'),    constants.UUID_TYPE_MEETING),
            (constants.EFILTER_PHONECALLS, _('Phone calls'), constants.UUID_TYPE_PHONECALL),
            (constants.EFILTER_TASKS,      _('Tasks'),       constants.UUID_TYPE_TASK),
        ]:
            create_efilter(
                pk, name=name, model=Activity, is_custom=False, user='admin',
                conditions=[
                    condition_handler.RegularFieldConditionHandler.build_condition(
                        model=Activity,
                        operator=operators.EqualsOperator,
                        field_name='type',
                        values=[act_types[atype_uuid].id],
                    ),
                ],
            )

        create_efilter(
            constants.EFILTER_PARTICIPATE, name=_('In which I participate'),
            model=Activity, is_custom=False, user='admin',
            conditions=[
                condition_handler.RelationSubFilterConditionHandler.build_condition(
                    model=Activity,
                    rtype=rt_obj_part_2_activity,
                    subfilter=EntityFilter.objects.get_latest_version(FILTER_CONTACT_ME),
                ),
            ],
        )

        # ---------------------------
        CustomFormConfigItem.objects.create_if_needed(
            descriptor=custom_forms.ACTIVITY_CREATION_CFORM,
        )
        CustomFormConfigItem.objects.create_if_needed(
            descriptor=custom_forms.ACTIVITY_CREATION_FROM_CALENDAR_CFORM,
        )
        CustomFormConfigItem.objects.create_if_needed(
            descriptor=custom_forms.UNAVAILABILITY_CREATION_CFORM,
        )
        CustomFormConfigItem.objects.create_if_needed(
            descriptor=custom_forms.ACTIVITY_EDITION_CFORM,
        )

        # ---------------------------
        SearchConfigItem.objects.create_if_needed(
            Activity, ['title', 'description', 'type__name'],
        )

        # ---------------------------
        create_svalue = SettingValue.objects.get_or_create
        create_svalue(key_id=setting_keys.review_key.id,        defaults={'value': True})
        create_svalue(key_id=setting_keys.auto_subjects_key.id, defaults={'value': True})

        # ---------------------------
        if not already_populated:
            # create_subtype(
            #     atype=unav_t, name=_('Holidays'), is_custom=True,
            #     pk='activities-activitysubtype_holidays',
            # )
            # create_subtype(
            #     atype=unav_t, name=_('Ill'), is_custom=True,
            #     pk='activities-activitysubtype_ill',
            # )
            create_subtype = ActivitySubType.objects.create
            create_subtype(
                type=unav_t, name=_('Holidays'), is_custom=True,
                uuid='d0408f78-77ba-4c49-9fa7-fc1e3455554e',
            )
            create_subtype(
                type=unav_t, name=_('Ill'), is_custom=True,
                uuid='09baec7a-b0ba-4c03-8981-84fc066d2970',
            )

            # create_subtype(
            #     atype=act_types[constants.ACTIVITYTYPE_TASK],
            #     name=_('Task'), is_custom=True,
            #     pk='activities-activitysubtype_task',
            # )
            create_subtype(
                type=act_types[constants.UUID_TYPE_TASK],
                name=_('Task'), is_custom=True,
                uuid='767b94e1-b366-4b97-8755-d719b268e402',
            )

            # gathering_t = act_types[constants.ACTIVITYTYPE_GATHERING]
            # for pk, name in [
            #     ('activities-activitysubtype_gathering', _('Gathering')),
            #     (
            #         'activities-activitysubtype_gathering_team',
            #         pgettext('activities-gathering', 'Team')
            #     ),
            #     (
            #         'activities-activitysubtype_gathering_internal',
            #         pgettext('activities-gathering', 'Internal')
            #     ),
            #     ('activities-activitysubtype_gathering_on_site', _('On the site')),
            #     ('activities-activitysubtype_gathering_remote',  _('Remote')),
            #     ('activities-activitysubtype_gathering_outside', _('Outside')),
            # ]:
            #     create_subtype(atype=gathering_t, pk=pk, name=name, is_custom=True)
            gathering_t = act_types[constants.UUID_TYPE_GATHERING]
            for uid, name in [
                ('75b957a2-4fe7-4b98-8493-3f95e43a4968', _('Gathering')),
                ('2147569e-7bc4-4b79-8760-844dc568c422', pgettext('activities-gathering', 'Team')),
                (
                    'e4ff08c8-80df-4528-bcc1-4f9d20c6fe61',
                    pgettext('activities-gathering', 'Internal')
                ),
                ('1c626935-d47a-4d9b-af4b-b90b8a71fc77', _('On the site')),
                ('8f003f06-f1ea-456e-90f3-82e8b8ef7424', _('Remote')),
                ('bc001a5c-eb90-4a3c-b703-afe347d3bf34', _('Outside')),
            ]:
                create_subtype(uuid=uid, type=gathering_t, name=name, is_custom=True)

            # show_t = act_types[constants.ACTIVITYTYPE_SHOW]
            # for pk, name in [
            #     ('activities-activitysubtype_show_exhibitor', _('Exhibitor')),
            #     ('activities-activitysubtype_show_visitor',   _('Visitor')),
            # ]:
            #     create_subtype(atype=show_t, pk=pk, name=name, is_custom=True)
            show_t = act_types[constants.UUID_TYPE_SHOW]
            for uid, name in [
                ('b75a663c-af2e-4440-89b3-2a75410cd55b', _('Exhibitor')),
                ('591b34b3-4226-48d4-a74d-d94665190b44', _('Visitor')),
            ]:
                create_subtype(uuid=uid, type=show_t, name=name, is_custom=True)

            # demo_t = act_types[constants.ACTIVITYTYPE_DEMO]
            # for pk, name in [
            #     ('activities-activitysubtype_demo',                 _('Demonstration')),
            #     ('activities-activitysubtype_demo_on_site',         _('On the site')),
            #     ('activities-activitysubtype_demo_outside',         _('Outside')),
            #     ('activities-activitysubtype_demo_videoconference', _('Videoconference')),
            # ]:
            #     create_subtype(atype=demo_t, pk=pk, name=name, is_custom=True)
            demo_t = act_types[constants.UUID_TYPE_DEMO]
            for uid, name in [
                ('c32a94c7-8a2a-4589-8b0d-6764c63fb659', _('Demonstration')),
                ('247902ed-05dd-4ba6-9cbd-ea43b7c996eb', _('On the site')),
                ('e22a2e5d-4349-4d44-bd77-21b1a10816d5', _('Outside')),
                ('3faf21bf-80b4-4182-b975-8146db2fb68b', _('Videoconference')),
            ]:
                create_subtype(uuid=uid, type=demo_t, name=name, is_custom=True)

            # ---------------------------
            create_mitem = MenuConfigItem.objects.create
            menu_container = create_mitem(
                entry_id=ContainerEntry.id,
                entry_data={'label': _('Activities')},
                order=10,
            )
            create_mitem(entry_id=menu.CalendarEntry.id,   order=10, parent=menu_container)
            create_mitem(entry_id=menu.ActivitiesEntry.id, order=20, parent=menu_container)
            create_mitem(entry_id=menu.PhoneCallsEntry.id, order=30, parent=menu_container)
            create_mitem(entry_id=menu.MeetingsEntry.id,   order=40, parent=menu_container)

            # ---------------------------
            LEFT = BrickDetailviewLocation.LEFT
            RIGHT = BrickDetailviewLocation.RIGHT

            BrickDetailviewLocation.objects.multi_create(
                defaults={'model': Activity, 'zone': LEFT},
                data=[
                    {'order': 5},
                    {'brick': core_bricks.CustomFieldsBrick, 'order':  40},
                    {'brick': bricks.RelatedCalendarBrick,   'order':  90},
                    {'brick': bricks.ParticipantsBrick,      'order': 100},
                    {'brick': bricks.SubjectsBrick,          'order': 120},
                    {'brick': core_bricks.PropertiesBrick,   'order': 450},
                    {'brick': core_bricks.RelationsBrick,    'order': 500},

                    {'brick': core_bricks.HistoryBrick, 'order': 20, 'zone': RIGHT},
                ],
            )

            if apps.is_installed('creme.assistants'):
                logger.info(
                    'Assistants app is installed'
                    ' => we use the assistants blocks on detail views'
                )

                import creme.assistants.bricks as a_bricks

                BrickDetailviewLocation.objects.multi_create(
                    defaults={'model': Activity, 'zone': RIGHT},
                    data=[
                        {'brick': a_bricks.TodosBrick,        'order': 100},
                        {'brick': a_bricks.MemosBrick,        'order': 200},
                        {'brick': a_bricks.AlertsBrick,       'order': 300},
                        {'brick': a_bricks.UserMessagesBrick, 'order': 400},
                    ],
                )

            if apps.is_installed('creme.documents'):
                # logger.info('Documents app is installed
                # => we use the documents block on detail views')

                from ..documents.bricks import LinkedDocsBrick

                BrickDetailviewLocation.objects.create_if_needed(
                    brick=LinkedDocsBrick, order=600, zone=RIGHT, model=Activity,
                )

            future_id = bricks.FutureActivitiesBrick.id
            past_id   = bricks.PastActivitiesBrick.id

            BrickDetailviewLocation.objects.multi_create(
                defaults={'zone': RIGHT},
                data=[
                    {'brick': future_id, 'order': 20, 'model': Contact},
                    {'brick': past_id,   'order': 21, 'model': Contact},
                    {'brick': future_id, 'order': 20, 'model': Organisation},
                    {'brick': past_id,   'order': 21, 'model': Organisation},
                ],
            )

            BrickHomeLocation.objects.create(brick_id=future_id, order=20)
            BrickHomeLocation.objects.create(brick_id=past_id,   order=21)

            # ---------------------------
            create_button = ButtonMenuItem.objects.create_if_needed
            create_button(button=buttons.AddRelatedActivityButton, order=10)
            create_button(button=buttons.AddMeetingButton,         order=11)
            create_button(button=buttons.AddPhoneCallButton,       order=12)