from django.forms import ModelForm
from .models import Endereco, Entrega


class FormularioEndereco(ModelForm):
    class Meta:
        model = Endereco

        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs.update({"class": "form-control"})


class FormularioEntrega(ModelForm):
    class Meta:
        model = Entrega
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs.update({"class": "form-control"})
