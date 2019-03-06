from django.forms import ModelForm

from .models import dbNames


class dbForm(ModelForm):

	class Meta:
		model = dbNames
		fields = "__all__"

