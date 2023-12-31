################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2009-2020  Hybird
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
import math
import importlib
from django.utils.translation import gettext as _
from PIL import ImageFile as PILImageFile
from django.core.exceptions import ImproperlyConfigured

from . import get_folder_model


def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        size, srepr = bytes / 1099511627776, "TB"
    elif bytes >= 1073741824:
        size, srepr = bytes / 1073741824, "GB"
    elif bytes >= 1048576:
        size, srepr = bytes / 1048576, "MB"
    elif bytes >= 1024:
        size, srepr = bytes / 1024, "KB"
    else:
        size, srepr = bytes, " bytes"
    return "%d%s" % (math.ceil(size), srepr)


def get_csv_folder_or_create(user):
    return get_folder_model().objects.get_or_create(
        title=_('CSV Documents'),
        defaults={
            'description':   _('Folder containing all the CSV documents used when importing data'),
            'parent_folder': None,
            'category':      None,
            'user':          user,
        },
    )[0]


def get_image_format(data):
    p = PILImageFile.Parser()
    p.feed(data)

    return p.close().format