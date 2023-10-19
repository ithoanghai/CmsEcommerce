from django.apps import AppConfig as BaseAppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from imagekit import register

from .utils import load_path_attr


class AppConfig(BaseAppConfig):
    name = "creme.news"
    label = "news"
    verbose_name = _("News")

    def ready(self):
        image_path = getattr(
            settings,
            "NEWS_IMAGE_THUMBNAIL_SPEC",
            "creme.news.specs.ImageThumbnail"
        )
        secondary_image_path = getattr(
            settings,
            "NEWS_SECONDARY_IMAGE_THUMBNAIL_SPEC",
            "creme.news.specs.SecondaryImageThumbnail"
        )

        image_spec_class = load_path_attr(image_path)
        secondary_image_spec_class = load_path_attr(secondary_image_path)

        register.generator("news:image:thumb", image_spec_class)
        register.generator("news:secondary_image:thumb", secondary_image_spec_class)
