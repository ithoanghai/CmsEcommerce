from __future__ import unicode_literals
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import gettext as _

from .models import Event


class PlanForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            "kind",
            "livemode",
            "customer_id",
            "account_id",
            "message"
        ]

    def save(self, commit=True):
        obj = super(PlanForm, self).save(commit=False)
        obj.applicant = self.user
        if commit:
            obj.save()
        return obj