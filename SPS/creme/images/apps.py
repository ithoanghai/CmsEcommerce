from django.apps import AppConfig as BaseAppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from imagekit import register

from ..utils import load_path_attr


class AppConfig(BaseAppConfig):
    name = "creme.images"
    label = "images"
    verbose_name = _("Images")

    def ready(self):
        thumbnail_path = getattr(
            settings,
            "IMAGES_THUMBNAIL_SPEC",
            "creme.images.specs.ImageThumbnail"
        )
        thumbnail_spec_class = load_path_attr(thumbnail_path)
        register.generator("creme.images:image:thumbnail", thumbnail_spec_class)

        list_thumbnail_path = getattr(
            settings,
            "IMAGES_LIST_THUMBNAIL_SPEC",
            "creme.images.specs.ImageListThumbnail"
        )
        list_thumbnail_spec_class = load_path_attr(list_thumbnail_path)
        register.generator("creme.images:image:list_thumbnail", list_thumbnail_spec_class)

        small_thumbnail_path = getattr(
            settings,
            "IMAGES_SMALL_THUMBNAIL_SPEC",
            "creme.images.specs.ImageSmallThumbnail"
        )
        small_thumbnail_spec_class = load_path_attr(small_thumbnail_path)
        register.generator("images:image:small_thumbnail", small_thumbnail_spec_class)

        medium_thumbnail_path = getattr(
            settings,
            "IMAGES_MEDIUM_THUMBNAIL_SPEC",
            "creme.images.specs.ImageMediumThumbnail"
        )
        medium_thumbnail_spec_class = load_path_attr(medium_thumbnail_path)
        register.generator("creme.images:image:medium_thumbnail", medium_thumbnail_spec_class)
