from django import forms
from django.utils.translation import gettext as _
from django.core.validators import URLValidator
from .models import BookmarkInstance


class BookmarkInstanceForm(forms.ModelForm):

    url = forms.URLField(label="URL", validators=[URLValidator()],
                         widget=forms.TextInput(attrs={"size": 40}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"size": 40}))
    redirect = forms.BooleanField(label="Redirect", required=False)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BookmarkInstanceForm, self).__init__(*args, **kwargs)
        # hack to order fields
        self.fields.keyOrder = ["url", "description", "redirect"]

    def clean(self):
        if not self.cleaned_data.get("url", None):
            return self.cleaned_data
        if BookmarkInstance.objects.filter(bookmark__url=self.cleaned_data["url"],
                                           user=self.user).count() > 0:
            raise forms.ValidationError(_("You have already bookmarked this link."))
        return self.cleaned_data

    def should_redirect(self):
        if self.cleaned_data["redirect"]:
            return True
        else:
            return False

    def save(self, commit=True):
        self.instance.url = self.cleaned_data["url"]
        return super(BookmarkInstanceForm, self).save(commit)

    class Meta:
        model = BookmarkInstance
        fields = [
            "url",
            "description",
            "redirect"
        ]
