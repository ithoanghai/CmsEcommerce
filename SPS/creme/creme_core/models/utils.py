################################################################################
#
# Copyright (c) 2016-2020 Hybird
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################

import itertools
from django.db import DEFAULT_DB_ALIAS

from django.contrib.admin.utils import NestedObjects

from typing import Callable

from django.db.models import Model

from ..utils import ellipsis


def get_related_objects(obj, using=DEFAULT_DB_ALIAS):
    # This code is based on https://github.com/makinacorpus/django-safedelete
    collector = NestedObjects(using=using)
    collector.collect([obj])

    def flatten(elem):
        if isinstance(elem, list):
            return itertools.chain.from_iterable(map(flatten, elem))
        elif obj != elem:
            return (elem,)
        return ()

    return flatten(collector.nested())


def assign_2_charfield(instance: Model,
                       field_name: str,
                       value: str,
                       truncate: Callable[[str, int], str] = ellipsis) -> None:
    field = instance._meta.get_field(field_name)
    setattr(instance, field_name, truncate(value, field.max_length))
