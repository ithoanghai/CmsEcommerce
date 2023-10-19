# Generated by Django 4.2.6 on 2023-10-17 15:32

import app_CMS.base.blocks
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import modelcluster.fields
import uuid
import wagtail.blocks
import wagtail.contrib.forms.models
import wagtail.contrib.routable_page.models
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.models
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogDetailPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('excerpt', wagtail.fields.RichTextField()),
                ('content', wagtail.fields.StreamField([('content_title', app_CMS.base.blocks.BlogContentTitleBlock()), ('code', app_CMS.base.blocks.BlogCodeBlock()), ('rich_text', app_CMS.base.blocks.BlogRichTextBlock()), ('image', app_CMS.base.blocks.BlogImageBlock())], null=True, use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogListPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='GenericSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_url', models.URLField(blank=True, verbose_name='Twitter URL')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub URL')),
                ('organisation_url', models.URLField(blank=True, verbose_name='Organisation URL')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='link_title')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='link_title')),
                ('link_url', models.CharField(blank=True, max_length=500)),
                ('open_in_new_tab', models.BooleanField(blank=True, default=False)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='CmsConfig.menu')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubMenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='link_title')),
                ('link_url', models.CharField(blank=True, max_length=500)),
                ('open_in_new_tab', models.BooleanField(blank=True, default=False)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_menu_items', to='CmsConfig.menuitem')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('introduction', models.TextField(blank=True, help_text='Text to describe the page')),
                ('body', wagtail.fields.StreamField([('heading_block', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('paragraph_block', wagtail.blocks.RichTextBlock(icon='pilcrow', template='blocks/paragraph_block.html')), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('block_quote', wagtail.blocks.StructBlock([('text', wagtail.blocks.TextBlock()), ('attribute_name', wagtail.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='blocks/embed_block.html'))], blank=True, use_json_field=True, verbose_name='Page body')),
                ('image', models.ForeignKey(blank=True, help_text='Landscape mode only; horizontal width between 1000px and 3000px.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_suffix', models.CharField(default='The Wagtail Bakery', help_text="The suffix for the title meta tag e.g. ' | The Wagtail Bakery'", max_length=255, verbose_name='Title suffix')),
                ('github', models.URLField(blank=True, help_text='Github URL', null=True)),
                ('twitter', models.URLField(blank=True, help_text='Twitter URL', null=True)),
                ('linkedin', models.URLField(blank=True, help_text='linkedin URL', null=True)),
                ('sitemap', models.URLField(blank=True, help_text='Sitemap rss.xml', null=True)),
                ('logo', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('live', models.BooleanField(default=True, editable=False, verbose_name='live')),
                ('has_unpublished_changes', models.BooleanField(default=False, editable=False, verbose_name='has unpublished changes')),
                ('first_published_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='first published at')),
                ('last_published_at', models.DateTimeField(editable=False, null=True, verbose_name='last published at')),
                ('go_live_at', models.DateTimeField(blank=True, null=True, verbose_name='go live date/time')),
                ('expire_at', models.DateTimeField(blank=True, null=True, verbose_name='expiry date/time')),
                ('expired', models.BooleanField(default=False, editable=False, verbose_name='expired')),
                ('locked', models.BooleanField(default=False, editable=False, verbose_name='locked')),
                ('locked_at', models.DateTimeField(editable=False, null=True, verbose_name='locked at')),
                ('first_name', models.CharField(max_length=254, verbose_name='First name')),
                ('last_name', models.CharField(max_length=254, verbose_name='Last name')),
                ('job_title', models.CharField(max_length=254, verbose_name='Job title')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('latest_revision', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.revision', verbose_name='latest revision')),
                ('live_revision', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.revision', verbose_name='live revision')),
                ('locked_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locked_%(class)ss', to=settings.AUTH_USER_MODEL, verbose_name='locked by')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
            bases=(wagtail.models.WorkflowMixin, wagtail.models.PreviewableMixin, wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('hero_text', models.CharField(help_text='Write an introduction for the bakery', max_length=255)),
                ('hero_cta', models.CharField(help_text='Text to display on Call to Action', max_length=255, verbose_name='Hero CTA')),
                ('body', wagtail.fields.StreamField([('heading_block', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('paragraph_block', wagtail.blocks.RichTextBlock(icon='pilcrow', template='blocks/paragraph_block.html')), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('block_quote', wagtail.blocks.StructBlock([('text', wagtail.blocks.TextBlock()), ('attribute_name', wagtail.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='blocks/embed_block.html'))], blank=True, use_json_field=True, verbose_name='Home content block')),
                ('promo_title', models.CharField(blank=True, help_text='Title to display above the promo copy', max_length=255)),
                ('promo_text', wagtail.fields.RichTextField(blank=True, help_text='Write some promotional copy', max_length=1000, null=True)),
                ('featured_section_1_title', models.CharField(blank=True, help_text='Title to display above the promo copy', max_length=255)),
                ('featured_section_2_title', models.CharField(blank=True, help_text='Title to display above the promo copy', max_length=255)),
                ('featured_section_3_title', models.CharField(blank=True, help_text='Title to display above the promo copy', max_length=255)),
                ('content', wagtail.fields.StreamField([('right_image_left_content', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('paragraph', wagtail.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('cta_url', wagtail.blocks.URLBlock(required=False)), ('cta_page', wagtail.blocks.PageChooserBlock(required=False)), ('cta_text', wagtail.blocks.CharBlock(default='Submit', max_length='50', required=False)), ('cta_image', wagtail.images.blocks.ImageChooserBlock(required=False))])))])), ('aboutapp', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('paragraph', wagtail.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('sub_heading', wagtail.blocks.CharBlock(required=False)), ('sub_paragraph', wagtail.blocks.RichTextBlock(required=False)), ('cta_url', wagtail.blocks.URLBlock(required=False)), ('cta_page', wagtail.blocks.PageChooserBlock(required=False)), ('cta_text', wagtail.blocks.CharBlock(default='Submit', max_length='50', required=False)), ('links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(required=False))])))])), ('count', wagtail.blocks.StructBlock([('links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('count', wagtail.blocks.CharBlock(default=85, required=False)), ('count_value', wagtail.blocks.CharBlock(required=False)), ('text', wagtail.blocks.CharBlock(required=False))])))])), ('appfeatures', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon', wagtail.blocks.CharBlock(required=False)), ('card_heading', wagtail.blocks.CharBlock(required=False)), ('card_description', wagtail.blocks.CharBlock(required=False))])))])), ('pricing', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('card_heading', wagtail.blocks.CharBlock(required=False)), ('card_price', wagtail.blocks.CharBlock(required=False)), ('card_description', wagtail.blocks.RichTextBlock(required=False)), ('cta_url', wagtail.blocks.URLBlock(required=False)), ('cta_page', wagtail.blocks.PageChooserBlock(required=False)), ('cta_text', wagtail.blocks.CharBlock(default='Choose Plan', max_length='50', required=False))])))])), ('carousel', wagtail.blocks.StructBlock([('sliders', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('description', wagtail.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('author', wagtail.blocks.CharBlock(required=False)), ('role', wagtail.blocks.CharBlock(required=False))])))])), ('leftimagerighttext', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('paragraph', wagtail.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('cta_url', wagtail.blocks.URLBlock(required=False)), ('cta_page', wagtail.blocks.PageChooserBlock(required=False)), ('cta_text', wagtail.blocks.CharBlock(default='Submit', max_length='50', required=False)), ('cta_image', wagtail.images.blocks.ImageChooserBlock(required=False))])))])), ('homeblog', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('blog_tag', wagtail.blocks.CharBlock(required=False)), ('blog_heading', wagtail.blocks.CharBlock(required=False)), ('cta_url', wagtail.blocks.URLBlock(required=False)), ('cta_page', wagtail.blocks.PageChooserBlock(required=False)), ('cta_text', wagtail.blocks.CharBlock(default='Read More', max_length='50', required=False))])))]))], null=True, use_json_field=True)),
                ('featured_section_1', models.ForeignKey(blank=True, help_text='First featured section for the homepage. Will display up to three child items.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Featured section 1')),
                ('featured_section_2', models.ForeignKey(blank=True, help_text='Second featured section for the homepage. Will display up to three child items.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Featured section 2')),
                ('featured_section_3', models.ForeignKey(blank=True, help_text='Third featured section for the homepage. Will display up to six child items.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Featured section 3')),
                ('hero_cta_link', models.ForeignKey(blank=True, help_text='Choose a page to link to for the Call to Action', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Hero CTA link')),
                ('image', models.ForeignKey(blank=True, help_text='Homepage image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('promo_image', models.ForeignKey(blank=True, help_text='Promo image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='GalleryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('introduction', models.TextField(blank=True, help_text='Text to describe the page')),
                ('body', wagtail.fields.StreamField([('heading_block', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('paragraph_block', wagtail.blocks.RichTextBlock(icon='pilcrow', template='blocks/paragraph_block.html')), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('block_quote', wagtail.blocks.StructBlock([('text', wagtail.blocks.TextBlock()), ('attribute_name', wagtail.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='blocks/embed_block.html'))], blank=True, use_json_field=True, verbose_name='Page body')),
                ('collection', models.ForeignKey(blank=True, help_text='Select the image collection for this gallery.', limit_choices_to=models.Q(('name__in', ['Root']), _negated=True), null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailcore.collection')),
                ('image', models.ForeignKey(blank=True, help_text='Landscape mode only; horizontal width between 1000px and 3000px.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, validators=[wagtail.contrib.forms.models.validate_to_address], verbose_name='to address')),
                ('from_address', models.EmailField(blank=True, max_length=255, verbose_name='from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='subject')),
                ('body', wagtail.fields.StreamField([('heading_block', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('paragraph_block', wagtail.blocks.RichTextBlock(icon='pilcrow', template='blocks/paragraph_block.html')), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('block_quote', wagtail.blocks.StructBlock([('text', wagtail.blocks.TextBlock()), ('attribute_name', wagtail.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='blocks/embed_block.html'))], use_json_field=True)),
                ('thank_you_text', wagtail.fields.RichTextField(blank=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.forms.models.FormMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('clean_name', models.CharField(blank=True, default='', help_text='Safe name of the form field, the label converted to ascii_snake_case', max_length=255, verbose_name='name')),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('hidden', 'Hidden field')], max_length=16, verbose_name='field type')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('default_value', models.TextField(blank=True, help_text='Default value. Comma or new line separated values supported for checkboxes.', verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='CmsConfig.formpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FooterText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('live', models.BooleanField(default=True, editable=False, verbose_name='live')),
                ('has_unpublished_changes', models.BooleanField(default=False, editable=False, verbose_name='has unpublished changes')),
                ('first_published_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='first published at')),
                ('last_published_at', models.DateTimeField(editable=False, null=True, verbose_name='last published at')),
                ('go_live_at', models.DateTimeField(blank=True, null=True, verbose_name='go live date/time')),
                ('expire_at', models.DateTimeField(blank=True, null=True, verbose_name='expiry date/time')),
                ('expired', models.BooleanField(default=False, editable=False, verbose_name='expired')),
                ('body', wagtail.fields.RichTextField()),
                ('latest_revision', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.revision', verbose_name='latest revision')),
                ('live_revision', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.revision', verbose_name='live revision')),
                ('locale', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale')),
            ],
            options={
                'verbose_name_plural': 'Footer Text',
                'abstract': False,
                'unique_together': {('translation_key', 'locale')},
            },
            bases=(wagtail.models.PreviewableMixin, models.Model),
        ),
    ]
