from django import forms
from .models import Ticket
from bson.objectid import ObjectId

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
        fields= ('name', 'content', 'location', 'urgency', 'status', 'category', 'department', 'deadline')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

    def is_valid(self):

        self.data._mutable = True
        self.data['location'] = ObjectId(self.data['location'])
        self.data['urgency'] = ObjectId(self.data['urgency'])
        self.data['status'] = ObjectId(self.data['status'])
        self.data['category'] = ObjectId(self.data['category'])
        self.data['department'] = ObjectId(self.data['department'])
        

        valid = super(TicketForm, self).is_valid()
        
        return valid
    