from django.forms import ModelForm

from .models import Group


class CreateGroup(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'time', 'day']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
