from django.forms import ModelForm
from .models import UsedProduct


class UsedForm(ModelForm):
    class Meta:
        model = UsedProduct
        fields = '__all__'