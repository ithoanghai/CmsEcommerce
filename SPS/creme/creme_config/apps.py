################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2015-2023  Hybird
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

from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

# flake8: noqa, because URL syntax is more readable with long lines
from django.apps import apps
from django.conf import settings
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from django.apps import AppConfig
from ..creme_core.core.loading import get_class
from ..creme_core.apps import CremeAppConfig


class CremeConfigConfig(CremeAppConfig):
    default = True
    name = 'creme.creme_config'
    verbose_name = _('General configuration')
    dependencies = ['creme.creme_core']
    credentials = CremeAppConfig.CRED_REGULAR

    VOTE_THRESHOLD = 3

    def all_apps_ready(self):
        super().all_apps_ready()

        self.hook_password_validators()

        from .registry import config_registry
        self.populate_config_registry(config_registry)

    # TODO: define our own classes?
    def hook_password_validators(self):
        from django.contrib.auth import password_validation

        # ---
        def minlen_get_help_text(this):
            return ngettext(
                'The password must contain at least %(min_length)d character.',
                'The password must contain at least %(min_length)d characters.',
                this.min_length,
            ) % {'min_length': this.min_length}

        password_validation.MinimumLengthValidator.get_help_text = minlen_get_help_text

        # ---
        def personal_get_help_text(self):
            return _(
                "The password can’t be too similar to the other personal information."
            )

        password_validation.UserAttributeSimilarityValidator.get_help_text = personal_get_help_text

        # ---
        def common_get_help_text(self):
            return _("The password can’t be a commonly used password.")

        password_validation.CommonPasswordValidator.get_help_text = common_get_help_text

        # ---
        def numeric_get_help_text(self):
            return _("The password can’t be entirely numeric.")

        password_validation.NumericPasswordValidator.get_help_text = numeric_get_help_text

    def populate_config_registry(self, config_registry):
        from ..creme_core.apps import creme_app_configs

        for app_config in creme_app_configs():
            config_registry.get_app_registry(app_config.label, create=True)

            register_creme_config = getattr(app_config, 'register_creme_config', None)

            if register_creme_config is not None:
                register_creme_config(config_registry)

    def register_creme_config(self, config_registry):
        from . import bricks

        config_registry.register_portal_bricks(bricks.ExportButtonBrick)

    def register_bricks(self, brick_registry):
        from . import bricks

        brick_registry.register(
            bricks.WorldSettingsBrick,
            bricks.SettingsBrick,
            bricks.PropertyTypesBrick,
            bricks.RelationTypesBrick,
            bricks.CustomRelationTypesBrick,
            bricks.SemiFixedRelationTypesBrick,
            bricks.CustomFieldsBrick,
            bricks.CustomEnumsBrick,
            bricks.CustomFormsBrick,
            bricks.BrickDetailviewLocationsBrick,
            bricks.BrickHomeLocationsBrick,
            bricks.BrickDefaultMypageLocationsBrick,
            bricks.BrickMypageLocationsBrick,
            bricks.RelationBricksConfigBrick,
            bricks.InstanceBricksConfigBrick,
            bricks.ExportButtonBrick,
            bricks.FieldsConfigsBrick,
            bricks.CustomBricksConfigBrick,
            bricks.MenuBrick,
            bricks.ButtonMenuBrick,
            bricks.UsersBrick,
            bricks.TeamsBrick,
            bricks.SearchConfigBrick,
            bricks.HistoryConfigBrick,
            bricks.UserRolesBrick,
            bricks.UserSettingValuesBrick,
            bricks.EntityFiltersBrick,
            bricks.HeaderFiltersBrick,
        )

    def register_menu_entries(self, menu_registry):
        from ..creme_core import menu as core_menu

        from . import menu

        menu_registry.register(menu.CremeConfigEntry)

        # Hook CremeEntry
        children = core_menu.CremeEntry.child_classes
        children.insert(
            children.index(core_menu.MyPageEntry),
            menu.TimezoneEntry,
        )
        children.insert(
            children.index(core_menu.MyJobsEntry) + 1,
            menu.MySettingsEntry,
        )

    #def for oscar
    def ready(self):
        from django.contrib.auth.forms import SetPasswordForm

        self.dashboard_app = apps.get_app_config('creme_core')

        #for oscar
        self.catalogue_app = apps.get_app_config('catalogue')
        self.customer_app = apps.get_app_config('customer')
        self.basket_app = apps.get_app_config('basket')
        self.checkout_app = apps.get_app_config('checkout')
        self.search_app = apps.get_app_config('search')
        self.offer_app = apps.get_app_config('offer')
        self.wishlists_app = apps.get_app_config('wishlists')

        self.password_reset_form = get_class('customer.forms', 'PasswordResetForm')
        self.set_password_form = SetPasswordForm

    def get_urls(self):
        from django.contrib.auth import views as auth_views

        from ..creme_core.views.decorators import login_forbidden

        urls = [
            path('dashboard/', self.dashboard_app.urls),  #shop dashboard

            path('', RedirectView.as_view(url=settings.OSCAR_HOMEPAGE), name='shop_home'),
            path('catalogue/', self.catalogue_app.urls),
            path('basket/', self.basket_app.urls),
            path('checkout/', self.checkout_app.urls),
            path('accounts/', self.customer_app.urls),
            path('search/', self.search_app.urls),
            path('offers/', self.offer_app.urls),
            path('wishlists/', self.wishlists_app.urls),

            # Password reset - as we're using Django's default view functions,
            # we can't namespace these urls as that prevents
            # the reverse function from working.
            path('password-reset/',
                login_forbidden(
                    auth_views.PasswordResetView.as_view(
                        form_class=self.password_reset_form,
                        success_url=reverse_lazy('password-reset-done'),
                        template_name='oscar/registration/password_reset_form.html'
                    )
                ),
                name='password-reset'),
            path('password-reset/done/',
                login_forbidden(auth_views.PasswordResetDoneView.as_view(
                    template_name='oscar/registration/password_reset_done.html'
                )),
                name='password-reset-done'),
            path('password-reset/confirm/<str:uidb64>/<str:token>/',
                login_forbidden(
                    auth_views.PasswordResetConfirmView.as_view(
                        form_class=self.set_password_form,
                        success_url=reverse_lazy('password-reset-complete'),
                        template_name='oscar/registration/password_reset_confirm.html'
                    )
                ),
                name='password-reset-confirm'),
            path('password-reset/complete/',
                login_forbidden(auth_views.PasswordResetCompleteView.as_view(
                    template_name='oscar/registration/password_reset_complete.html'
                )),
                name='password-reset-complete'),
        ]
        return urls
        #return self.post_process_urls(urls)

