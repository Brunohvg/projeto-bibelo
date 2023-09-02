from django.forms import ModelForm, Textarea
from .models import Entrega, Endereco
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class FormularioEndereco(ModelForm):
    class Meta:
        model = Endereco

        fields = "__all__"


"""    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs.update({"class": "form-control"})"""


class FormularioEntrega(ModelForm):
    class Meta:
        model = Entrega
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['info_adicional'].widget.attrs.update(
            {'rows': 4})  # Define o número máximo de linhas

        self.helper = FormHelper()
        self.helper.layout = Layout(
            # ... outros campos
            'info_adicional',
            # ... outros campos
        )
