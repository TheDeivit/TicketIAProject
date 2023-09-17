from django import forms
from .models import Ticket, Category, Profile
from bson.objectid import ObjectId
from django.forms import FileField
from django.contrib.auth.models import User

class TicketForm(forms.ModelForm):
    technician = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Tecnicos'))
    #DA ESTILO AL FORM
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        #evidence = forms.FileField(label='Subir evidencias', required=False)

        for f in iter(self.fields):
            self.fields[f].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Ticket
        fields= ('name', 'content', 'location', 'urgency', 'status', 'specialCase', 'category', 'department', 'deadline')#, 'evidence'
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

    def is_valid(self):

        self.data._mutable = True
        self.data['location'] = ObjectId(self.data['location'])
        self.data['urgency'] = ObjectId(self.data['urgency'])
        self.data['status'] = ObjectId(self.data['status'])
        self.data['specialCase'] = ObjectId(self.data['specialCase'])
        self.data['category'] = ObjectId(self.data['category'])
        self.data['department'] = ObjectId(self.data['department'])
        

        valid = super(TicketForm, self).is_valid()
        
        return valid

class CategoryForm(forms.ModelForm):
    #DA ESTILO AL FORM
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for f in iter(self.fields):
            self.fields[f].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Category
        fields= ('name', 'categorytype')#, 'evidence'
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

    def is_valid(self):

        self.data._mutable = True
        self.data['categorytype'] = ObjectId(self.data['categorytype'])
        

        valid = super(CategoryForm, self).is_valid()
        
        return valid

class ProfileForm(forms.ModelForm):
    username = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Tecnicos'))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for f in iter(self.fields):
            self.fields[f].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Profile
        fields = ('name','username', 'specialty', 'location')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }
    def is_valid(self):

        self.data._mutable = True
        self.data['specialty'] = ObjectId(self.data['specialty'])
        self.data['location'] = ObjectId(self.data['location'])

        valid = super(ProfileForm, self).is_valid()
        
        return valid