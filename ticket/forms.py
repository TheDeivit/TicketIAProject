from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    
    #DA ESTILO AL FORM
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        for f in iter(self.fields):
            self.fields[f].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Ticket
        fields= ('name', 'content', 'location')