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
import arrow
from functools import partial

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.transaction import atomic
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from django.conf import settings

from ...creme_core.common.utils import CURRENCY_CODES, SOURCES, STAGES
from ...creme_core.models import base as core_models, fields as core_fields, Account, Tags
from ...creme_core.models.entity import CremeEntity
from ...creme_core.models.currency import Currency
from ...creme_core.models.deletion import CREME_REPLACE_NULL
from ...creme_core.constants import DEFAULT_CURRENCY_PK
from ...persons import get_organisation_model
from ...persons.workflow import transform_target_into_prospect
from ...persons.models import Organisation, Profile, Contact, Teams
from .. import constants


class SalesPhase(core_models.MinionModel):
    name = models.CharField(_('Name'), max_length=100)
    order = core_fields.BasicAutoField()
    color = core_fields.ColorField(default=core_fields.ColorField.random)

    won  = models.BooleanField(pgettext_lazy('opportunities-sales_phase', 'Won'),  default=False)
    lost = models.BooleanField(pgettext_lazy('opportunities-sales_phase', 'Lost'), default=False)

    creation_label = pgettext_lazy('opportunities-sales_phase', 'Create a phase')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'opportunities'
        verbose_name = _('Sale phase')
        verbose_name_plural = _('Sale phases')
        ordering = ('order',)

    def clean(self):
        super().clean()

        if self.won and self.lost:
            raise ValidationError(_('A phase can not be won and lost at the same time.'))


class Origin(core_models.MinionModel):
    name = models.CharField(_('Origin'), max_length=100)

    creation_label = pgettext_lazy('opportunities-origin', 'Create an origin')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'opportunities'
        verbose_name = _('Origin of opportunity')
        verbose_name_plural = _('Origins of opportunity')
        ordering = ('name',)


class AbstractOpportunity(CremeEntity):
    name = models.CharField(_('Name of the Opportunity'), max_length=100)
    account = models.ForeignKey(Account,related_name="opportunities",on_delete=models.CASCADE,blank=True, null=True,)
    stage = models.CharField(pgettext_lazy("Stage of Opportunity", "Stage"), max_length=64, choices=STAGES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CODES, blank=True, null=True )
    amount = models.DecimalField(_("Opportunity Amount"), decimal_places=2, max_digits=12, blank=True, null=True)
    lead_source = models.CharField(_("Source of Lead"), max_length=255, choices=SOURCES, blank=True, null=True)
    probability = models.IntegerField(default=0, blank=True, null=True)
    contacts = models.ManyToManyField(Contact)
    closed_by = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="oppurtunity_closed_by",)
    # closed_on = models.DateTimeField(blank=True, null=True)
    closed_on = models.DateField(blank=True, null=True)
    assigned_to = models.ManyToManyField(Profile, related_name="opportunity_assigned_to")
    created_by = models.ForeignKey(Profile,related_name="opportunity_created_by",on_delete=models.SET_NULL,null=True,)
    created_on = models.DateTimeField(_("Created on"), auto_now=True)
    is_active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)
    teams = models.ManyToManyField(settings.PERSONS_TEAM_MODEL, related_name="oppurtunity_teams")
    org = models.ForeignKey(settings.PERSONS_ORGANISATION_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="oppurtunity_org",)

    reference = models.CharField(_('Reference'), max_length=100, blank=True,).set_tags(optional=True)

    estimated_sales = models.PositiveIntegerField(_('Estimated sales'), blank=True, null=True,).set_tags(optional=True)
    made_sales = models.PositiveIntegerField(_('Made sales'), blank=True, null=True,).set_tags(optional=True)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'),default=DEFAULT_CURRENCY_PK, on_delete=models.PROTECT,)

    sales_phase = models.ForeignKey(SalesPhase, verbose_name=_('Sales phase'), on_delete=models.PROTECT,)
    chance_to_win = models.PositiveIntegerField(_(r'% of chance to win'), blank=True, null=True,).set_tags(optional=True)

    expected_closing_date = models.DateField(_('Expected closing date'), blank=True, null=True,).set_tags(optional=True)
    closing_date = models.DateField(_('Actual closing date'), blank=True, null=True,).set_tags(optional=True)

    origin = models.ForeignKey(Origin, verbose_name=_('Origin'),blank=True, null=True, on_delete=CREME_REPLACE_NULL,).set_tags(optional=True)

    first_action_date = models.DateField(_('Date of the first action'), blank=True, null=True,).set_tags(optional=True)

    creation_label = _('Create an opportunity')
    save_label     = _('Save the opportunity')

    search_score = 100

    _opp_emitter = None
    _opp_target  = None
    _opp_target_rel = None

    class Meta:
        abstract = True
        app_label = 'opportunities'
        verbose_name = _('Opportunity')
        verbose_name_plural = _('Opportunities')
        ordering = ('name',"-created_on")

    def __str__(self):
        return self.name

    def _clean_emitter_n_target(self):
        # if not self.pk:  # Creation
        # NB: if the user (which is required) is not set, an error will be
        #     raised before anyway. In bulk-edition, an empty instance is
        #     built to check some errors (before true instances are validated),
        #     & the following validation was annoying.
        if not self.pk and self.user_id:  # Creation
            if not self._opp_emitter:
                raise ValidationError(_('Emitter is required.'))

            if not self._opp_target:
                raise ValidationError(_('Target is required.'))

    def _pre_delete(self):
        for relation in self.relations.filter(
            type__in=(constants.REL_SUB_TARGETS, constants.REL_OBJ_EMIT_ORGA),
        ):
            relation._delete_without_transaction()

    def _pre_save_clone(self, source):
        self.emitter = source.emitter
        self.target  = source.target

    def clean(self):
        self._clean_emitter_n_target()
        super().clean()

    def get_absolute_url(self):
        return reverse('opportunities__view_opportunity', args=(self.id,))

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        return Profile.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.assigned_to.values_list("id", flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return Profile.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.assigned_to.values_list("id", flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return Profile.objects.filter(id__in=list(user_ids))

    @staticmethod
    def get_create_absolute_url():
        return reverse('opportunities__create_opportunity')

    def get_edit_absolute_url(self):
        return reverse('opportunities__edit_opportunity', args=(self.id,))

    @staticmethod
    def get_lv_absolute_url():
        return reverse('opportunities__list_opportunities')

    def get_total(self):
        if self.made_sales:
            return self.made_sales
        else:
            return self.estimated_sales or 0

    def get_total_with_tax(self):
        tax = 1 + core_models.Vat.objects.default().value / 100

        if self.made_sales:
            return self.made_sales * tax
        else:
            return (self.estimated_sales or 0) * tax

    @property
    def emitter(self):
        if not self._opp_emitter:
            self._opp_emitter = get_organisation_model().objects.get(
                relations__type=constants.REL_SUB_EMIT_ORGA,
                relations__object_entity=self.id,
            )
            # TODO ? (2 queries, but we could group with target maybe...)
            # self._opp_emitter = self.get_related_entities(
            #     constants.REL_OBJ_EMIT_ORGA,
            # )[0]

        return self._opp_emitter

    @emitter.setter
    def emitter(self, organisation):
        assert self.pk is None, \
            'Opportunity.emitter(setter): emitter is already saved (can not change any more).'
        self._opp_emitter = organisation

    @property
    def target(self):
        if not self._opp_target:
            self._opp_target_rel = rel = self.get_relations(constants.REL_SUB_TARGETS)[0]
            self._opp_target = rel.real_object

        return self._opp_target

    @target.setter
    def target(self, person):
        if self.pk:  # Edition:
            old_target = self.target
            if old_target != person:
                self._opp_target = person
        else:
            self._opp_target = person

    @atomic
    def save(self, *args, **kwargs):
        create_relation = partial(
            core_models.Relation.objects.create, object_entity=self, user=self.user,
        )
        target = self._opp_target

        if not self.pk:  # Creation
            self._clean_emitter_n_target()

            super().save(*args, **kwargs)

            # TODO: set *_rel attributes (see billing.Base)
            create_relation(subject_entity=self._opp_emitter, type_id=constants.REL_SUB_EMIT_ORGA)
            create_relation(subject_entity=target,            type_id=constants.REL_OBJ_TARGETS)

            transform_target_into_prospect(self._opp_emitter, target, self.user)
        else:
            super().save(*args, **kwargs)

            old_relation = self._opp_target_rel

            if old_relation and old_relation.object_entity_id != target.id:
                old_relation.delete()
                # TODO: set *_rel attribute (see billing.Base)
                create_relation(subject_entity=self._opp_target, type_id=constants.REL_OBJ_TARGETS)
                transform_target_into_prospect(self.emitter, target, self.user)

    if apps.is_installed('creme.billing'):
        def get_current_quote_ids(self):
            from django.contrib.contenttypes.models import ContentType

            from ...billing import get_quote_model

            ct = ContentType.objects.get_for_model(get_quote_model())

            return core_models.Relation.objects.filter(
                object_entity=self.id,
                type=constants.REL_SUB_CURRENT_DOC,
                subject_entity__entity_type=ct,
            ).values_list('subject_entity_id', flat=True)


class Opportunity(AbstractOpportunity):
    class Meta(AbstractOpportunity.Meta):
        swappable = 'OPPORTUNITIES_OPPORTUNITY_MODEL'
