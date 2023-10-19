from __future__ import unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.translation import gettext as _
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
    PageChooserPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    Collection,
    DraftStateMixin,
    LockableMixin,
    Orderable,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    WorkflowMixin,
)
from wagtail.search import index
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import render

from .blocks import BaseStreamBlock
from . import blocks

@register_snippet
class Person(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
    index.Indexed,
    ClusterableModel,
):
    """
    A Django model to store Person objects.
    It is registered using `register_snippet` as a function in wagtail_hooks.py
    to allow it to have a menu item within a custom menu item group.

    `Person` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """

    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("first_name"),
                        FieldPanel("last_name"),
                    ]
                )
            ],
            "Name",
        ),
        FieldPanel("job_title"),
        FieldPanel("image"),
        PublishingPanel(),
    ]

    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.FilterField("job_title"),
        index.AutocompleteField("first_name"),
        index.AutocompleteField("last_name"),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition("fill-50x50").img_tag()
        except:  # noqa: E722
            return ""

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + [("blog_post", _("Blog post"))]

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_preview_template(self, request, mode_name):
        from app_CMS.blog.models import BlogPage

        if mode_name == "blog_post":
            return BlogPage.template
        return "base/preview/person.html"

    def get_preview_context(self, request, mode_name):
        from app_CMS.blog.models import BlogPage

        context = super().get_preview_context(request, mode_name)
        if mode_name == self.default_preview_mode:
            return context

        page = BlogPage.objects.filter(blog_person_relationship__person=self).first()
        if page:
            # Use the page authored by this person if available,
            # and replace the instance from the database with the edited instance
            page.authors = [
                self if author.pk == self.pk else author for author in page.authors()
            ]
            # The authors() method only shows live authors, so make sure the instance
            # is included even if it's not live as this is just a preview
            if not self.live:
                page.authors.append(self)
        else:
            # Otherwise, get the first page and simulate the person as the author
            page = BlogPage.objects.first()
            page.authors = [self]

        context["page"] = page
        return context

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"


class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):
    """
    This provides editable text for the site footer. Again it is registered
    using `register_snippet` as a function in wagtail_hooks.py to be grouped
    together with the Person model inside the same main menu item. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"


class StandardPage(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )
    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
    ]


class HomePage(Page):
    """
    The Home Page. This looks slightly more complicated than it is. You can
    see if you visit your site and edit the homepage that it is split between
    a:
    - Hero area
    - Body area
    - A promotional area
    - Moveable featured site sections
    """

    # Hero section of HomePage
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )
    hero_text = models.CharField(
        max_length=255, help_text="Write an introduction for the bakery"
    )
    hero_cta = models.CharField(
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    # Body section of the HomePage
    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Home content block",
        blank=True,
        use_json_field=True,
    )

    # Promo section of the HomePage
    promo_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Promo image",
    )
    promo_title = models.CharField(
        blank=True, max_length=255, help_text="Title to display above the promo copy"
    )
    promo_text = RichTextField(
        null=True, blank=True, max_length=1000, help_text="Write some promotional copy"
    )

    # Featured sections on the HomePage
    # You will see on templates/base/home_page.html that these are treated
    # in different ways, and displayed in different areas of the page.
    # Each list their children items that we access via the children function
    # that we define on the individual Page models e.g. BlogIndexPage
    featured_section_1_title = models.CharField(
        blank=True, max_length=255, help_text="Title to display above the promo copy"
    )
    featured_section_1 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="First featured section for the homepage. Will display up to "
        "three child items.",
        verbose_name="Featured section 1",
    )

    featured_section_2_title = models.CharField(
        blank=True, max_length=255, help_text="Title to display above the promo copy"
    )
    featured_section_2 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Second featured section for the homepage. Will display up to "
        "three child items.",
        verbose_name="Featured section 2",
    )

    featured_section_3_title = models.CharField(
        blank=True, max_length=255, help_text="Title to display above the promo copy"
    )
    featured_section_3 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Third featured section for the homepage. Will display up to "
        "six child items.",
        verbose_name="Featured section 3",
    )

    content = StreamField(
        [
            ("right_image_left_content", blocks.RightImageLeftText()),
            ("aboutapp", blocks.AboutApp()),
            ("count", blocks.Count()),
            ("appfeatures", blocks.AppFeatures()),
            ("pricing", blocks.Pricing()),
            ("carousel", blocks.Carousel()),
            ("leftimagerighttext", blocks.LeftImageRightText()),
            ("homeblog", blocks.HomeBlog()),
        ],
        null=True,
        blank=False,
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                FieldPanel("content"),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_cta"),
                        FieldPanel("hero_cta_link"),
                    ]
                ),
            ],
            heading="Hero section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("promo_image"),
                FieldPanel("promo_title"),
                FieldPanel("promo_text"),
            ],
            heading="Promo section",
        ),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                MultiFieldPanel(
                    [
                        FieldPanel("featured_section_1_title"),
                        FieldPanel("featured_section_1"),
                    ]
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("featured_section_2_title"),
                        FieldPanel("featured_section_2"),
                    ]
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("featured_section_3_title"),
                        FieldPanel("featured_section_3"),
                    ]
                ),
            ],
            heading="Featured homepage sections",
        ),
    ]

    def __str__(self):
        return self.title


# class BlogCategory(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(max_length=255)

#     def __str__(self):
#         return self.name

#     panels = [FieldPanel("name"), FieldPanel("slug")]

#     class Meta:
#         ordering = ["name"]

# register_snippet(BlogCategory)


class BlogListPage(RoutablePageMixin, Page):

    template = "cms/blog/blog_list_page.html"
    max_count = 1
    intro = RichTextField(blank=True)

    @route(r"^(?P<page_num>\d+)")
    def get_context(self, request, *args, **kwargs):
        # Update context to include only published posts, ordered by reverse-chron
        # request.session.clear()
        context = super().get_context(request, *args, **kwargs)

        all_posts = (
            BlogDetailPage.objects.live().public().order_by("-first_published_at")
        )

        paginator = Paginator(all_posts, 1)

        page = int(kwargs.get("page_num", 1))

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        # context["category_count"] = BlogCategory.objects.annotate(
        #     num_posts=Count("blogdetailpage")
        # )
        context["posts"] = posts
        # context["categories"] = BlogCategory.objects.all()
        if kwargs.get("page_num"):
            return render(request, "cms/blog/blog_list_page.html", context)
        else:
            return context

    # @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    # def category_view(self, request, cat_slug):
    #     context = self.get_context(request)
    #     category = BlogCategory.objects.get(slug=cat_slug)
    #     category_posts = (
    #         BlogDetailPage.objects.live().public().filter(category=category)
    #     )

    #     paginator = Paginator(category_posts, 10)

    #     # page = int(kwargs.get('page_num', 1))
    #     page = 1

    #     try:
    #         category_posts = paginator.page(page)
    #     except PageNotAnInteger:
    #         category_posts = paginator.page(1)
    #     except EmptyPage:
    #         category_posts = paginator.page(paginator.num_pages)

    #     context["category_posts"] = category_posts
    #     context["current_category"] = category
    #     return render(request, "blog/blog_category.html", context)

    # content_panels = Page.content_panels + [
    #     FieldPanel("intro", classname="full"),
    # ]


class BlogDetailPage(Page):
    template = "cms/blog/blog_detail_page.html"
    excerpt = RichTextField()
    # show_legend = models.BooleanField(default=False)
    # category = models.ForeignKey(BlogCategory, null=True, on_delete=models.SET_NULL)

    content = StreamField(
        [
            ("content_title", blocks.BlogContentTitleBlock()),
            ("code", blocks.BlogCodeBlock()),
            ("rich_text", blocks.BlogRichTextBlock()),
            ("image", blocks.BlogImageBlock()),
        ],
        null=True,
        blank=False,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        # FieldPanel("category"),
        # FieldPanel("show_legend"),
        FieldPanel("excerpt"),
        FieldPanel("content"),
    ]


class GalleryPage(Page):
    """
    This is a page to list locations from the selected Collection. We use a Q
    object to list any Collection created (/admin/collections/) even if they
    contain no items. In this demo we use it for a GalleryPage,
    and is intended to show the extensibility of this aspect of Wagtail
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and " "3000px.",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Select the image collection for this gallery.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("collection"),
    ]

    # Defining what content type can sit under the parent. Since it's a blank
    # array no subpage can be added
    subpage_types = []


class FormField(AbstractFormField):
    """
    Wagtailforms is a module to introduce simple forms on a Wagtail site. It
    isn't intended as a replacement to Django's form support but as a quick way
    to generate a general purpose data-collection form or contact form
    without having to write code. We use it on the site for a contact form. You
    can read more about Wagtail forms at:
    https://docs.wagtail.org/en/stable/reference/contrib/forms/index.html
    """

    page = ParentalKey("FormPage", related_name="form_fields", on_delete=models.CASCADE)


class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(BaseStreamBlock(), use_json_field=True)
    thank_you_text = RichTextField(blank=True)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("image"),
        FieldPanel("body"),
        InlinePanel("form_fields", heading="Form fields", label="Field"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address"),
                        FieldPanel("to_address"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]


# ============================  Navigation Menu   ===============================================


@register_snippet
class Menu(ClusterableModel):
    """The main menu clusterable model."""

    title = models.CharField(_("link_title"), max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug"),
            ],
            heading="Menu",
        ),
        InlinePanel("menu_items", label="Menu Item"),
    ]

    def __str__(self):
        return self.title


class MenuItem(Orderable, ClusterableModel):
    """The First level menu of the Navigationbar."""

    link_title = models.CharField(_("link_title"), blank=True, null=True, max_length=50)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("link_title"),
                FieldPanel("link_url"),
                PageChooserPanel("link_page"),
                FieldPanel("open_in_new_tab"),
            ],
            heading="MenuItem",
        ),
        InlinePanel("sub_menu_items", label="Sub Menu Item"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return "#"

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing Title"


class SubMenuItem(Orderable):
    """The Second level menu of the Navigationbar."""

    link_title = models.CharField(_("link_title"), blank=True, null=True, max_length=50)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )

    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("MenuItem", related_name="sub_menu_items")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("link_title"),
                FieldPanel("link_url"),
                PageChooserPanel("link_page"),
                FieldPanel("open_in_new_tab"),
            ],
            heading="SubMenuItem",
        ),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return "#"

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing Title"




@register_setting
class GenericSettings(ClusterableModel, BaseGenericSetting):
    twitter_url = models.URLField(verbose_name="Twitter URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    organisation_url = models.URLField(verbose_name="Organisation URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("github_url"),
                FieldPanel("twitter_url"),
                FieldPanel("organisation_url"),
            ],
            heading="Social Settings",
        )
    ]


@register_setting
class SiteSettings(BaseSiteSetting):
    """Site settings for our custom website."""
    title_suffix = models.CharField(
        verbose_name="Title suffix",
        max_length=255,
        help_text="The suffix for the title meta tag e.g. ' | The Wagtail Bakery'",
        default="The Wagtail Bakery",
    )

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    github = models.URLField(blank=True, null=True, help_text="Github URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    linkedin = models.URLField(blank=True, null=True, help_text="linkedin URL")
    sitemap = models.URLField(blank=True, null=True, help_text="Sitemap rss.xml")

    panels = [
        MultiFieldPanel(
            [   FieldPanel("title_suffix"),
                FieldPanel("github"),
                FieldPanel("twitter"),
                FieldPanel("linkedin"),
                FieldPanel("sitemap"),
                FieldPanel("logo"),
            ],
            heading="Site Settings",
        )
    ]
