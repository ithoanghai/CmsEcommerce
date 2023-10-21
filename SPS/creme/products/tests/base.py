from functools import partial
from unittest import skipIf

from ...creme_core.auth.entity_credentials import EntityCredentials
from ...creme_core.models import SetCredentials
from ...creme_core.tests.views.base import MassImportBaseTestCaseMixin
from ...documents import get_document_model
from ...documents.tests.base import _DocumentsTestCase

from .. import product_model_is_custom, service_model_is_custom

skip_product_tests = product_model_is_custom()
skip_service_tests = service_model_is_custom()


def skipIfCustomProduct(test_func):
    return skipIf(skip_product_tests, 'Custom Product model in use')(test_func)


def skipIfCustomService(test_func):
    return skipIf(skip_service_tests, 'Custom Service model in use')(test_func)


class _ProductsTestCase(_DocumentsTestCase, MassImportBaseTestCaseMixin):
    EXTRA_CATEGORY_KEY = 'cform_extra-products_subcategory'

    def login_as_basic_user(self, creatable_model):
        # user = self.login(
        #     is_superuser=False, allowed_apps=['products', 'documents'],
        #     creatable_models=[creatable_model, get_document_model()],
        # )
        user = self.login_as_standard(
            allowed_apps=['products', 'documents'],
            creatable_models=[creatable_model, get_document_model()],
        )

        create_sc = partial(SetCredentials.objects.create, role=user.role)
        create_sc(
            value=(
                EntityCredentials.VIEW
                | EntityCredentials.CHANGE
                | EntityCredentials.DELETE
                | EntityCredentials.LINK
                | EntityCredentials.UNLINK
            ),
            set_type=SetCredentials.ESET_OWN,
        )
        create_sc(
            value=(
                EntityCredentials.VIEW
                | EntityCredentials.CHANGE
                | EntityCredentials.DELETE
                | EntityCredentials.UNLINK
                # | EntityCredentials.LINK
            ),
            set_type=SetCredentials.ESET_ALL,
        )

        return user
